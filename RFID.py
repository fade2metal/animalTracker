class RFID:

    def from_hex(c: str) -> int:
        """Konvertiert ein einzelnes Hex-Zeichen in eine Zahl"""
        if '0' <= c <= '9':
            return ord(c) - ord('0')
        return ord(c.upper()) - ord('A') + 10

    def decode_fdxb_ascii_string(ascii_str: str):
        """Dekodiert eine ISO11784 UID aus einer ASCII-Hex-Zeichenkette"""
        # Nur die relevanten 10+4 Zeichen extrahieren (Tag ID + Country ID)
        tag_chars = ascii_str[0:10]
        country_chars = ascii_str[10:14]

        # Berechne Tag ID (von rechts nach links)
        tag_id = 0
        for c in reversed(tag_chars):
            tag_id = (tag_id << 4) + RFID.from_hex(c)

        # Berechne Country ID
        country_id = 0
        for c in reversed(country_chars):
            country_id = (country_id << 4) + RFID.from_hex(c)

        # ISO-Format: country code (3-stellig), Tiernummer (12-stellig)
        return f"{country_id:03d}{tag_id:012d}"