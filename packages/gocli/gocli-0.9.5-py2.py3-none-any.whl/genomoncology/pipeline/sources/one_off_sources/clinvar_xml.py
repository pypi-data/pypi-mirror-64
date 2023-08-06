import xml.etree.cElementTree as etree

VARIANT_TYPE_BLACKLIST = [
    "Phase unknown",
    "Haplotype",
    "fusion",
    "Inversion",
    "Translocation",
    "Complex",
    "copy number loss",
    "copy number gain",
    "Microsatellite",
    "CompoundHeterozygote",
    "Diplotype",
]

ASSEMBLY = "Assembly"
CLINICAL_ASSERTION = "ClinicalAssertion"
CLINICAL_ASSERTION_ID = "ClinicalAssertionID"
CLINICAL_ASSERTION_LIST = "ClinicalAssertionList"
CLINVAR_ACCESSION = "ClinVarAccession"
DESCRIPTION = "Description"
ELEMENT_VALUE = "ElementValue"
ID = "ID"
GENE = "Gene"
GENE_LIST = "GeneList"
GRCH_37 = "GRCh37"
INCLUDED_RECORD = "IncludedRecord"
INTERPRETATION = "Interpretation"
INTERPRETATIONS = "Interpretations"
INTERPRETED_CONDITION = "InterpretedCondition"
INTERPRETED_CONDITION_LIST = "InterpretedConditionList"
INTERPRETED_RECORD = "InterpretedRecord"
LOCATION = "Location"
MAPPING_REF = "MappingRef"
MAPPING_VALUE = "MappingValue"
MED_GEN = "MedGen"
NAME = "Name"
OBSERVED_IN = "ObservedIn"
OBSERVED_IN_LIST = "ObservedInList"
ORIGIN = "Origin"
PREFERRED = "Preferred"
PROTEIN_CHANGE = "ProteinChange"
RCV_ACCESSION = "RCVAccession"
RCV_LIST = "RCVList"
REVIEW_STATUS = "ReviewStatus"
SAMPLE = "Sample"
SEQUENCE_LOCATION = "SequenceLocation"
SIMPLE_ALLELE = "SimpleAllele"
SUBMITTER_NAME = "SubmitterName"
TRAIT = "Trait"
TRAIT_MAPPING = "TraitMapping"
TRAIT_MAPPING_LIST = "TraitMappingList"
TRAIT_SET = "TraitSet"
VARIATION_ARCHIVE = "VariationArchive"
VARIATION_ID = "VariationID"
VARIATION_TYPE = "VariationType"
XREF_LIST = "XRefList"
XREF = "XRef"


class ClinvarXMLSource:
    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        return self.parse_clinvar_xml()

    def create_combined_xref(self, interpreted_record):
        total_xref_val = []
        try:
            xrefs = (
                interpreted_record.find(SIMPLE_ALLELE)
                .find(XREF_LIST)
                .findall(XREF)
            )
            for xref in xrefs:
                db_vals = [xref.attrib.get("DB"), xref.attrib.get("Type")]
                db_str = (
                    "_".join(db_vals) if db_vals[1] is not None else db_vals[0]
                )
                total_xref_val.append(f"{db_str}:{xref.attrib.get('ID')}")
            return "|".join(total_xref_val)
        except Exception:
            return None

    def get_origin_vals_list(self, clinical_assertion):
        return [
            oi.find(SAMPLE).find(ORIGIN).text
            for oi in clinical_assertion.find(OBSERVED_IN_LIST).findall(
                OBSERVED_IN
            )
        ]

    def get_submission_conditions(
        self, clinical_assertion, interpreted_record
    ):
        try:
            all_trait_mappings = interpreted_record.find(
                TRAIT_MAPPING_LIST
            ).findall(TRAIT_MAPPING)
            conditions = self.get_conditions_from_trait_mapping(
                clinical_assertion, all_trait_mappings
            )
        except Exception:
            conditions = self.get_conditions_from_traitset(clinical_assertion)
        return conditions

    def get_conditions_from_trait_mapping(self, assertion, all_trait_mappings):
        assertion_id = assertion.attrib.get(ID)
        conditions = []
        for trait_mapping in all_trait_mappings:
            has_assertion = (
                trait_mapping.attrib.get(CLINICAL_ASSERTION_ID) == assertion_id
            )
            is_preferred = (
                trait_mapping.attrib.get(MAPPING_REF, False) == PREFERRED
            )
            if has_assertion and not is_preferred:
                conditions.append(trait_mapping.find(MED_GEN).attrib.get(NAME))
            elif has_assertion and is_preferred:
                conditions.append(trait_mapping.attrib.get(MAPPING_VALUE))
        # if an assertion has multiple diseases associated,
        # we went them as a comma seperated string.
        if len(conditions) > 1:
            conditions = [", ".join(conditions)]
        return conditions

    def get_conditions_from_traitset(self, clinical_assertion):
        try:
            element_values = (
                clinical_assertion.find(TRAIT_SET)
                .find(TRAIT)
                .find(NAME)
                .findall(ELEMENT_VALUE)
            )
        except Exception:
            return None
        if len(element_values) > 1:
            conditions = [
                e.text
                for e in element_values
                if e.attrib.get("Type") == "Preferred"
            ]
        else:
            conditions = [element_values[0].text]
        conditions = self.clean_string_list(conditions)
        return conditions

    def get_interpreted_conditions(self, rcv_accessions):
        interpreted_conditions = []
        for rcva in rcv_accessions:
            conditions = rcva.find(INTERPRETED_CONDITION_LIST).findall(
                INTERPRETED_CONDITION
            )
            if len(conditions) > 1:
                multiple_conditions = [
                    condition.text for condition in conditions
                ]
                interpreted_conditions.append(", ".join(multiple_conditions))
            else:
                interpreted_conditions.extend(conditions)
        return self.clean_string_list(interpreted_conditions)

    def clean_string_list(self, value_list):
        result = []
        for value in value_list:
            if isinstance(value, etree.Element):
                words = (
                    value.text.replace("\r", "").replace("\n", "").split(" ")
                )
            else:
                words = value.replace("\r", "").replace("\n", "").split(" ")
            result.append(" ".join([w for w in words if len(w) > 0]))
        return result

    def get_alteration_string(self, interpreted_record):
        gene_names = []
        try:
            protein_change = (
                interpreted_record.find(SIMPLE_ALLELE)
                .find(PROTEIN_CHANGE)
                .text
            )
        except Exception:
            protein_change = None
        try:
            genes = (
                interpreted_record.find(SIMPLE_ALLELE)
                .find(GENE_LIST)
                .findall(GENE)
            )
        except Exception:
            genes = None
        if genes and protein_change:
            for g in genes:
                gene = g.attrib.get("Symbol")
                gene_names.append(f"{gene} {protein_change}")
                return "".join(gene_names)
        else:
            return None

    def create_csra(self, interpreted_record):
        try:
            sequence_locations = (
                interpreted_record.find(SIMPLE_ALLELE)
                .find(LOCATION)
                .findall(SEQUENCE_LOCATION)
            )
            if sequence_locations:
                valid_sequence_locations = [
                    sl
                    for sl in sequence_locations
                    if sl.attrib.get(ASSEMBLY) == GRCH_37
                ]
                for sl in valid_sequence_locations:
                    chr, positionVCF = (
                        sl.attrib.get("Chr"),
                        sl.attrib.get("positionVCF"),
                    )
                    referenceAllele, alternateAllele = (
                        sl.attrib.get("referenceAlleleVCF"),
                        sl.attrib.get("alternateAlleleVCF"),
                    )
                    if referenceAllele == alternateAllele or not all(
                        [chr, positionVCF, referenceAllele, alternateAllele]
                    ):
                        return None
                    else:
                        return f"chr{chr}|{positionVCF}|"\
                               f"{referenceAllele}|{alternateAllele}|GRCh37"
            else:
                return None
        except Exception:
            return None

    def get_CLNSIG__mstring(self, interpretations):
        result = []
        for interpretation in interpretations:
            result = [
                i for i in interpretation.find(DESCRIPTION).text.split(",")
            ]
        return result

    def iterate_individual_submissions(  # pragma: no mccabe
        self, clinical_assertions, record, interpreted_record
    ):
        record["all_submission_interpretations__mstring"] = []
        record["all_submission_review_statuses__mstring"] = []
        record["all_submission_conditions__mstring"] = []
        record["all_submission_submitter__mstring"] = []
        record["all_submission_origin__mstring"] = []
        for assertion in clinical_assertions:
            try:
                description = (
                    assertion.find(INTERPRETATION).find(DESCRIPTION).text
                )
                record["all_submission_interpretations__mstring"].append(
                    description
                )
            except Exception:
                pass
            review_status = assertion.find(REVIEW_STATUS).text
            submission_conditions = self.get_submission_conditions(
                assertion, interpreted_record
            )
            submitter_names = assertion.find(CLINVAR_ACCESSION).attrib.get(
                SUBMITTER_NAME
            )
            submission_origins = (
                assertion.find(OBSERVED_IN_LIST)
                .find(OBSERVED_IN)
                .find(SAMPLE)
                .find(ORIGIN)
                .text
            )
            if review_status is not None:
                record["all_submission_review_statuses__mstring"].append(
                    review_status
                )
            if submission_conditions is not None:
                record["all_submission_conditions__mstring"].extend(
                    submission_conditions
                )
            if submitter_names is not None:
                record["all_submission_submitter__mstring"].append(
                    submitter_names
                )
            if submission_origins is not None:
                record["all_submission_origin__mstring"].append(
                    submission_origins
                )
        return record

    def should_parse_varchive(self, varchive):
        interpreted_record = varchive.find(INTERPRETED_RECORD)
        hgvs_g = self.create_csra(interpreted_record)
        is_missing_hgvs_and_alteration = (
            hgvs_g is None
            and self.get_alteration_string(interpreted_record) is None
        )
        if (
            varchive.attrib.get(VARIATION_TYPE) in VARIANT_TYPE_BLACKLIST
            or varchive.find(INCLUDED_RECORD)
            or is_missing_hgvs_and_alteration
        ):
            return False
        else:
            return True

    def var_archive_parse(self, variation_archive):  # pragma: no mccabe
        # common tree elements
        interpreted_record = variation_archive.find(INTERPRETED_RECORD)
        interpretations = interpreted_record.find(INTERPRETATIONS).findall(
            INTERPRETATION
        )
        clinical_assertions = interpreted_record.find(
            CLINICAL_ASSERTION_LIST
        ).findall(CLINICAL_ASSERTION)
        rcv_accessions = interpreted_record.find(RCV_LIST).findall(
            RCV_ACCESSION
        )

        # values
        clinsig = self.get_CLNSIG__mstring(interpretations)
        variation_id = variation_archive.attrib.get(VARIATION_ID)
        review_statuses = [interpreted_record.find(REVIEW_STATUS).text]
        clnvi = [self.create_combined_xref(interpreted_record)]
        clndn = self.get_interpreted_conditions(rcv_accessions)
        gene_protein_change = self.get_alteration_string(interpreted_record)
        alteration_string = (
            gene_protein_change
            if gene_protein_change
            else self.create_csra(interpreted_record)
        )
        hgvs_g = self.create_csra(interpreted_record)

        # build top-level result dict with fields that could be parsed
        record = {}
        if clinsig is not None:
            record["CLNSIG__mstring"] = clinsig
        if variation_id is not None:
            record["variant_ID__string"] = variation_id
        if review_statuses is not None:
            record["CLNREVSTAT__mstring"] = review_statuses
        if clnvi is not None:
            record["CLNVI__mstring"] = clnvi
        if clndn is not None:
            record["CLNDN__mstring"] = clndn
        if alteration_string:
            record["alteration__string"] = alteration_string
        if hgvs_g:
            record["hgvs_g"] = hgvs_g
        record = self.iterate_individual_submissions(
            clinical_assertions, record, interpreted_record
        )
        return record

    def determine_and_parse_record(self, variation_archive):
        if self.should_parse_varchive(variation_archive):
            return self.var_archive_parse(variation_archive)
        else:
            return None

    def parse_clinvar_xml(self):  # pragma: no mccabe
        parse_error_var_ids = []
        try:
            for event, elem in etree.iterparse(
                self.file_path, events=("start", "end")
            ):
                if event == "end" and elem.tag == VARIATION_ARCHIVE:
                    if self.should_parse_varchive(elem):
                        try:
                            yield self.var_archive_parse(elem)
                            elem.clear()
                        except Exception:
                            parse_error_var_ids.append(
                                elem.attrib.get(VARIATION_ID)
                            )
                    else:
                        elem.clear()
                        continue
                else:
                    continue
            if len(parse_error_var_ids) > 0:
                print(
                    "\n\nHere are the variation ids of "
                    "records in which a parsing error occurred..."
                )
                for id in parse_error_var_ids:
                    print(f"{id}\n")

        except etree.ParseError:
            print("Parse error. Check the format of your file.")
            exit()
