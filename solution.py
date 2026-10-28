# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14       # 대출 기간 (반납 기한 = 빌린 날 + 14)
MAX_LOANS = 3        # 한 사람이 동시에 빌릴 수 있는 최대 권수


def _is_day(value):
    """1 이상의 정수인지 확인. True/False는 파이썬에서 정수 취급되지만 여기서는 날짜로 보지 않음."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


class LibraryLoan:
    def __init__(self):
        # 대출 중인 책: book_id -> (빌린 사람, 빌린 날, 반납 기한)
        self.loans = {}
        # 대출 정지 기간 목록: (이름, 시작일, 마지막 날)  — 시작일~마지막 날 모두 대출 불가
        self.suspensions = []

    def _loans_of(self, name):
        return [(book_id, due) for book_id, (who, _, due) in self.loans.items() if who == name]

    def _is_suspended(self, name, day):
        return any(who == name and start <= day <= end for who, start, end in self.suspensions)

    def borrow(self, book_id, name, day):
        if book_id not in BOOKS:              # 1. 없는 책
            return False
        if not _is_day(day):                  # 2. 날짜가 1 이상의 정수가 아님
            return False
        if book_id in self.loans:             # 3. 이미 대출 중
            return False
        mine = self._loans_of(name)
        if len(mine) >= MAX_LOANS:            # 4. 이미 3권
            return False
        if any(day > due for _, due in mine):  # 5. 기한 지난 책을 갖고 있음
            return False
        if self._is_suspended(name, day):     # 6. 대출 정지 기간
            return False
        self.loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if not _is_day(day):
            return -1
        if book_id not in BOOKS or book_id not in self.loans:
            return -1
        who, borrowed_day, due = self.loans[book_id]
        if who != name or day < borrowed_day:
            return -1
        del self.loans[book_id]
        overdue = max(0, day - due)
        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 대출 정지 (겹치면 자연히 더 늦게 끝나는 쪽이 적용됨)
            self.suspensions.append((name, day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        return sorted(self._loans_of(name), key=lambda item: (item[1], item[0]))
