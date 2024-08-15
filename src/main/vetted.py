from .states import get_states_from_conf


class Vetted:

    @staticmethod
    def get_clinicians_url():
        url = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/clinicians?'
        default_search_params = 'hasMessaged=false&isLead=false'
        states_ids = get_states_from_conf()
        if states_ids:
            for state_id in states_ids:
                param = 'licensedStatesIds=' + state_id + '&'
                url = url + param
        url = url + default_search_params
        return url

    @staticmethod
    def get_convo_url() -> str:
        url = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/conversations?conversation='
        return url
