from abc import ABC, abstractmethod
from pandas import isnull
import regex as re

class BusinessRule(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def is_valid(self, value):
        pass

    @abstractmethod
    def get_description(self):
        pass


class NotNullRule(BusinessRule):

    def __init__(self):
        super(NotNullRule, self).__init__('Nicht NULL')

    def is_valid(self, value):
        return not isnull(value)

    def get_description(self):
        return "Wert muss befüllt sein"


class RegExPatternMatchingRule(BusinessRule):

    def __init__(self, pattern="*", dropna=False):
        super(RegExPatternMatchingRule, self).__init__("RegEx-Übereinstimmung")
        self.pattern = pattern
        self.regex = re.compile(self.pattern)
        self.dropna = dropna

    def is_valid(self, value):
        if self.dropna and isnull(value):
            return True
        return self.regex.match(str(value))

    def get_description(self):
        return "Wert muss Regulärem Ausdruck '{regex}' entsprechen".format(
            regex = self.pattern
        )


class EmailRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*|\[[\t -Z^-~]*])"
        super(EmailRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "Email-RegEx-Übereinstimmung (nach RFC 5322)"


class CWEmailRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^\p{L}+(-\p{L}+)*.\p{L}+(-\p{L}+)*@controlware.(de|at)$"
        super(CWEmailRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "CW-Email-RegEx-Übereinstimmung"


class PhoneRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^\+(?:[0-9]\x20?){6,14}[0-9]$"
        super(PhoneRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "Mobilnummer-RegEx-Übereinstimmung (nach ITU-T E.164)"


class LastNameRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^(\p{Ll}{3,} |d'){0,1}\p{Lu}\p{Ll}+((-|\x20)\p{Lu}\p{Ll}+)*$"
        super(LastNameRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "Nachname-RegEx-Übereinstimmung"


class FirstNameRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^\p{Lu}\p{Ll}*((\x20|-)\p{Lu}\p{Ll}*)*$"
        super(FirstNameRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "Vorname-RegEx-Übereinstimmung"


class GermanDateRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^\d{2}\.\d{2}\.\d{4}$"
        super(GermanDateRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "GermanDate-RegEx-Übereinstimmung"


class DateTimeRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^(([0-9]{4}-[0-9]{1,2})-([0-9]{1,2})) (([01][0-9]|[2][0-3]):([0-5][0-9]):[0-5][0-9].[0-9]{9})$"
        super(DateTimeRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "DateTime-RegEx-Übereinstimmung"


class DateTimeMEZRegExPatternMatchingRule(RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^(([0-9]{4}-[0-9]{1,2})-([0-9]{1,2})) (([01][0-9]|[2][0-3]):([0-5][0-9]):[0-5][0-9])$"
        super(DateTimeMEZRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "DateTime_MEZ-RegEx-Übereinstimmung"


class TwoLetterCountryCodeRegExPatternMatchingRule (RegExPatternMatchingRule):

    def __init__(self, dropna=False):
        pattern = "^[A-Z]{2}$"
        super(TwoLetterCountryCodeRegExPatternMatchingRule, self).__init__(pattern=pattern, dropna=dropna)
        self.name = "TwoLetterCountryCode-RegEx-Übereinstimmung (nach ISO 3166-1 alpha-2)"


class DomainListMatchingRule(BusinessRule):

    def __init__(self, values=[], dropna=False):
        super(DomainListMatchingRule, self).__init__("Domänen-Übereinstimmung")
        self.values = values
        self.dropna = dropna

    def is_valid(self, value):
        if(self.dropna and isnull(value)):
            return True
        return str(value) in self.values

    def get_description(self):
        return "Wert muss einem Wert aus der folgenden Liste entsprechen: {}".format(
            self.__get_value_list_as_string()
        )

    def __get_value_list_as_string(self):
        list_as_enumeration = "["
        for value in self.values:
            list_as_enumeration += "<br/>&nbsp;&nbsp;&nbsp;'{}', ".format(value)
        list_as_enumeration += "<br/>]"
        return list_as_enumeration


class TwoLetterCountryCodeDomainListMatchingRule(DomainListMatchingRule):

    def __init__(self, dropna=False):
        two_letter_country_code_list = [
            "AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR", "AM", "AW", "AU", "AT", "AZ", "BH", "BS",
            "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO", "BN", "BG", "BF",
            "BI", "KH", "CM", "CA", "CV", "KY", "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR",
            "CI", "HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE", "ET", "FK",
            "FO", "FJ", "FI", "FR", "GF", "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU",
            "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN", "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM",
            "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS", "LR",
            "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX",
            "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG",
            "NU", "NF", "MP", "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA",
            "RE", "RO", "RU", "RW", "BL", "SH", "KN", "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC",
            "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES", "LK", "SD", "SR", "SJ", "SZ", "SE", "CH",
            "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE",
            "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"
        ]
        super(TwoLetterCountryCodeDomainListMatchingRule, self).__init__(values=two_letter_country_code_list, dropna=dropna)
        self.name = "TwoLetterCountryCode-Domänenübereinstimmung (nach ISO 3166-1 alpha-2)"

    def get_description(self):
        return "Wert muss einem Wert aus der Liste der Two-Letter-Country-Codes entsprechen (nach ISO 3166-1 alpha-2)"


class NoFoldingWhiteSpacesRule(BusinessRule):

    def __init__(self):
        super(NoFoldingWhiteSpacesRule, self).__init__("Keine ummschließenden Leerzeichen")

    def is_valid(self, value):
        return len(str(value).strip()) == len(str(value))

    def get_description(self):
        return "Wert darf keine umschließenden Leerzeichen enthalten"