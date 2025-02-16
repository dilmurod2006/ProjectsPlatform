def get_test_serializer(test: dict) -> dict:
    return {
        # "id": str(test.get("_id")),
        "user_id": test.get("user_id"),  # test["user_id"] ham ishlaydi
        "titul_id": test.get("titul_id"),
        "qiymat": test.get("qiymat"),
        "sana": test.get("sana")
    }
