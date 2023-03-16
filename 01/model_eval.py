import random


class SomeModel:
    def predict(self, message: str) -> float:
        return random.random()


def predict_message_mood(
        message: str,
        model: SomeModel,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    if bad_thresholds > good_thresholds:
        raise ValueError("bad_thresholds не может быть больше, чем "
                         "good_thresholds")
    mark = model.predict(message)
    if mark < bad_thresholds:
        return "неуд"
    elif mark > good_thresholds:
        return "отл"
    else:
        return "норм"
