#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import TextIO

from src.model.document import Document
from src.writer.tagvalue.annotation_writer import write_annotation
from src.writer.tagvalue.creation_info_writer import write_creation_info
from src.writer.tagvalue.extracted_licensing_info_writer import write_extracted_licensing_info
from src.writer.tagvalue.file_writer import write_file
from src.writer.tagvalue.package_writer import write_package
from src.writer.tagvalue.relationship_writer import write_relationship
from src.writer.tagvalue.snippet_writer import write_snippet
from src.writer.tagvalue.tagvalue_writer_helper_functions import write_separator, scan_relationships, \
    determine_files_containing_snippets, write_optional_heading, write_list_of_elements


def write_document_to_file(document: Document, file_name: str):
    with open(file_name, "w") as out:
        write_document(document, out)


def write_document(document: Document, text_output: TextIO):
    """
    Write a SPDX tag value document.
    - document - src.document instance.
    - text_output - file like object that will be written to.
    """

    text_output.write("## Document Information\n")
    # Write out creation info
    write_creation_info(document.creation_info, text_output)
    write_separator(text_output)

    # Write sorted annotations
    write_optional_heading(document.annotations, "## Annotations\n", text_output)
    write_list_of_elements(document.annotations, write_annotation, text_output, True)

    relationships_to_write, contained_files_by_package_id = scan_relationships(document.relationships,
                                                                               document.packages, document.files)
    contained_snippets_by_file_id = determine_files_containing_snippets(document.snippets, document.files)
    packaged_file_ids = [file.spdx_id for files_list in contained_files_by_package_id.values()
                         for file in files_list]
    filed_snippet_ids = [snippet.spdx_id for snippets_list in contained_snippets_by_file_id.values()
                         for snippet in snippets_list]

    # Write Relationships
    write_optional_heading(relationships_to_write, "## Relationships\n", text_output)
    write_list_of_elements(relationships_to_write, write_relationship, text_output)
    write_separator(text_output)

    # Write snippet info
    for snippet in document.snippets:
        if snippet.spdx_id not in filed_snippet_ids:
            write_snippet(snippet, text_output)
            write_separator(text_output)

    # Write file info
    for file in document.files:
        if file.spdx_id not in packaged_file_ids:
            write_file(file, text_output)
            write_separator(text_output)
            if file.spdx_id in contained_snippets_by_file_id:
                write_list_of_elements(contained_snippets_by_file_id[file.spdx_id], write_snippet, text_output, True)

    # Write package info
    for package in document.packages:
        write_package(package, text_output)
        write_separator(text_output)
        if package.spdx_id in contained_files_by_package_id:
            for file in contained_files_by_package_id[package.spdx_id]:
                write_file(file, text_output)
                write_separator(text_output)
                if file.spdx_id in contained_snippets_by_file_id:
                    write_list_of_elements(contained_snippets_by_file_id[file.spdx_id], write_snippet, text_output, True)
                    break

    write_optional_heading(document.extracted_licensing_info, "## License Information\n", text_output)
    write_list_of_elements(document.extracted_licensing_info, write_extracted_licensing_info, text_output, True)
