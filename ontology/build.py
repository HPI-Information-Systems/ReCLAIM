import os

from pipeline.combine import get_combined_graph
from pipeline.error import BuildError
from pipeline.steps import run_all as run_all_steps

try:
    ontology = get_combined_graph()
    run_all_steps(ontology)

    current_directory_path = os.path.dirname(__file__)
    output_path = os.path.join(current_directory_path, "dist")

    os.makedirs(output_path, exist_ok=True)

    ontology.serialize(
        destination=os.path.join(output_path, "combined_schema.ttl"), format="turtle"
    )

except BuildError as e:
    e.print()
    exit(1)
