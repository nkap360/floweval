"""
Utility to generate and inspect DeepEval Goldens from documents.

Prerequisites:
    pip install deepeval chromadb langchain-core langchain-community langchain-text-splitters

Environment:
    configured from .env
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Any, Dict, Union

import logging

from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig

# ---------------------------------------------------------------------
# Logging that can be connected to loguru, structlog, etc.
# ---------------------------------------------------------------------
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
    )


@dataclass
class GoldensSummary:
    """Short summary of what has been generated"""
    num_documents: int
    document_paths: List[str]
    total_goldens: int
    with_expected_output: int
    without_expected_output: int


def _coerce_document_paths(
    document_paths: Union[str, Sequence[str]]
) -> List[str]:
    """Normalise doc path and coerce it in the list"""
    if isinstance(document_paths, str):
        return [document_paths]
    return list(document_paths)


def generate_goldens_from_documents(
    document_paths: Union[str, Sequence[str]],
    *,
    include_expected_output: bool = True,
    max_goldens_per_context: int = 2,
    # i make sure they're optional
    critic_model: Optional[str] = None,
    encoding: Optional[str] = None,
    max_contexts_per_document: int = 3,
    min_contexts_per_document: int = 1,
    max_context_length: int = 3,
    min_context_length: int = 1,
    chunk_size: int = 1024,
    chunk_overlap: int = 0,
    context_quality_threshold: float = 0.5,
    context_similarity_threshold: float = 0.5,
    max_retries: int = 3,
    embedder: Optional[str] = "text-embedding-3-small",
    # synthesizer options
    synthesizer_model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate one or more Goldens from one or many documents .

    Parameters
    ----------
    document_paths:
        Chemin (str) ou liste de chemins vers les documents.
        Types supportés : .txt, .docx, .pdf, .md, .markdown, .mdx
    include_expected_output:
        Si True, deepeval génère aussi expected_output pour chaque Golden.
    max_goldens_per_context:
        Nombre max de goldens synthétiques par contexte.
        Rappel: nb max final = max_goldens_per_context * max_contexts_per_document.
    critic_model:
        Modèle utilisé pour scorer la qualité des contextes
        (ex: "gpt-4.1") ou instance DeepEvalBaseLLM.
    encoding:
        Encodage forcé pour les fichiers texte. Si None → auto-détection.
    max_contexts_per_document / min_contexts_per_document:
        Borne haute / basse de contextes par document.
    max_context_length / min_context_length:
        Longueur (en nb de chunks) des contextes.
    chunk_size:
        Taille des chunks (en tokens) lors du parsing.
    chunk_overlap:
        Recouvrement entre chunks successifs (en tokens).
    context_quality_threshold:
        Score minimal de qualité (0–1) pour accepter un contexte.
    context_similarity_threshold:
        Seuil minimal de similarité cosinus pour regrouper les chunks.
    max_retries:
        Nombre max de tentatives pour trouver un contexte/cluster satisfaisant.
    embedder:
        Modèle d’embedding OpenAI ou DeepEvalBaseEmbeddingModel custom.
    synthesizer_model:
        Modèle du Synthesizer (ex: "gpt-4.1"). Si None, deepeval utilisera sa valeur par défaut.

    Returns
    -------
    dict:
        {
          "goldens": <liste de goldens>,
          "summary": GoldensSummary(...),
          "context_construction_config": <ContextConstructionConfig>
        }
    """
    doc_paths = _coerce_document_paths(document_paths)

    logger.info("Starting Golden generation from documents")
    logger.info("Documents: %s", doc_paths)
    logger.info(
        "Params: include_expected_output=%s, max_goldens_per_context=%s",
        include_expected_output,
        max_goldens_per_context,
    )

    # -----------------------------------------------------------------
    # 1. Construire la config de construction de contexte
    # -----------------------------------------------------------------
    context_config_kwargs = {
        "max_contexts_per_document": max_contexts_per_document,
        "min_contexts_per_document": min_contexts_per_document,
        "max_context_length": max_context_length,
        "min_context_length": min_context_length,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "context_quality_threshold": context_quality_threshold,
        "context_similarity_threshold": context_similarity_threshold,
        "max_retries": max_retries,
    }

    # Smiley(*-*) Je ne passe critic_model / encoding / embedder que s’ils sont fournis 
    if critic_model is not None:
        context_config_kwargs["critic_model"] = critic_model
    if encoding is not None:
        context_config_kwargs["encoding"] = encoding
    if embedder is not None:
        context_config_kwargs["embedder"] = embedder

    context_config = ContextConstructionConfig(**context_config_kwargs)
    logger.info("ContextConstructionConfig created: %s", context_config)

    # -----------------------------------------------------------------
    # 2. Je construis le Synthesizer
    # -----------------------------------------------------------------
    if synthesizer_model:
        logger.info("Instantiating Synthesizer with model='%s'", synthesizer_model)
        synthesizer = Synthesizer(model=synthesizer_model)
    else:
        logger.info("Instantiating Synthesizer with default model")
        synthesizer = Synthesizer()

    # -----------------------------------------------------------------
    # 3. AppeJ'appelle generate_goldens_from_docs()
    # -----------------------------------------------------------------
    logger.info("Calling synthesizer.generate_goldens_from_docs()")
    goldens = synthesizer.generate_goldens_from_docs(
        document_paths=doc_paths,
        include_expected_output=include_expected_output,
        max_goldens_per_context=max_goldens_per_context,
        context_construction_config=context_config,
    )

    # -----------------------------------------------------------------
    # 4. Construire un petit résumé
    # -----------------------------------------------------------------
    total_goldens = len(goldens)
    with_expected_output = 0
    without_expected_output = 0

    # On ne fait aucune hypothèse forte sur la forme exacte des objets Golden,
    # on vérifie juste la présence d’un attribut/clé expected_output.
    for g in goldens:
        expected = getattr(g, "expected_output", None)
        if expected is None and isinstance(g, dict):
            expected = g.get("expected_output")

        if expected:
            with_expected_output += 1
        else:
            without_expected_output += 1

    summary = GoldensSummary(
        num_documents=len(doc_paths),
        document_paths=doc_paths,
        total_goldens=total_goldens,
        with_expected_output=with_expected_output,
        without_expected_output=without_expected_output,
    )

    logger.info("Generated %d goldens from %d document(s)", total_goldens, len(doc_paths))
    logger.info(
        "Goldens with expected_output=%d, without_expected_output=%d",
        with_expected_output,
        without_expected_output,
    )

    return {
        "goldens": goldens,
        "summary": summary,
        "context_construction_config": context_config,
    }


# ---------------------------------------------------------------------
# Petit CLI pour tester rapidement depuis le terminal
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Generate DeepEval Goldens from documents."
    )
    parser.add_argument(
        "document_paths",
        nargs="+",
        help="Chemin(s) vers les documents (.txt, .pdf, .docx, .md, .markdown, .mdx)",
    )
    parser.add_argument(
        "--include-expected-output",
        action="store_true",
        default=True,
        help="Générer aussi expected_output (par défaut: True).",
    )
    parser.add_argument(
        "--max-goldens-per-context",
        type=int,
        default=2,
        help="Nombre max de goldens par contexte (défaut: 2).",
    )
    parser.add_argument(
        "--max-contexts-per-document",
        type=int,
        default=3,
        help="Nombre max de contextes par document (défaut: 3).",
    )

    args = parser.parse_args()

    result = generate_goldens_from_documents(
        document_paths=args.document_paths,
        include_expected_output=args.include_expected_output,
        max_goldens_per_context=args.max_goldens_per_context,
        max_contexts_per_document=args.max_contexts_per_document,
    )

    # On affiche juste un résumé JSON "propre" pour inspection rapide
    summary_dict = {
        "summary": result["summary"].__dict__,
        "num_goldens": len(result["goldens"]),
    }
    print(json.dumps(summary_dict, indent=2, ensure_ascii=False))
