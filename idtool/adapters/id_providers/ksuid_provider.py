import ksuid

class KSUIDIdProvider:
    name = "ksuid"

    def generate_id(self) -> str:
        return str(ksuid.ksuid())