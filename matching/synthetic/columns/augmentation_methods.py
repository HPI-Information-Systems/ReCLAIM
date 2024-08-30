class AugmentationMethods:
    def __init__(
        self,
        exp_name_override: str = None,
        use_deletion: bool = False,
        use_shuffle: bool = False,
        use_append_random_significant_words: bool = False,
        use_translations: bool = False,
        use_typos: bool = False,
        use_append_random_date: bool = False,
        use_abbreviations: bool = False,
        use_synonyms: bool = False,
        use_antonyms: bool = False,
    ):
        self.exp_name_override = exp_name_override

        self.use_deletion = use_deletion
        self.use_shuffle = use_shuffle
        self.use_append_random_significant_words = use_append_random_significant_words
        self.use_translations = use_translations
        self.use_typos = use_typos
        self.use_append_random_date = use_append_random_date
        self.use_abbreviations = use_abbreviations
        self.use_synonyms = use_synonyms
        self.use_antonyms = use_antonyms

    def format_str(self) -> str:
        if self.exp_name_override is not None:
            return self.exp_name_override
        
        methods_str_list = []
        if self.use_deletion:
            methods_str_list.append("Delete")
        if self.use_shuffle:
            methods_str_list.append("Shuffle")
        if self.use_append_random_significant_words:
            methods_str_list.append("Append_Words")
        if self.use_translations:
            methods_str_list.append("Translations")
        if self.use_typos:
            methods_str_list.append("Typos")
        if self.use_append_random_date:
            methods_str_list.append("Append_Dates")
        if self.use_abbreviations:
            methods_str_list.append("Abbreviations")
        if self.use_synonyms:
            methods_str_list.append("Synonyms")
        if self.use_antonyms:
            methods_str_list.append("Antonyms")

        return ".".join(methods_str_list)
