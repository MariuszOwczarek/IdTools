import ulid

class ULIDIdProvider:
    name = "ulid"

    def generate_id(self) -> str:
        return str(ulid.new())  # ✅ poprawnie z nowym API