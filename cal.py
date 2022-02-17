import calendar


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)  # 일요일을 시작 기점으로 하게끔
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)  # 해당 월의 weeklist 반환
        days = []
        for week in weeks:
            for day, week_day in week:
                days.append(day)
        return days

    def get_month(self):
        return self.months[self.month - 1]
