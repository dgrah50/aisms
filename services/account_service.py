from tortoise.exceptions import DoesNotExist

from models.models import Account


class AccountService:
    @staticmethod
    async def register_or_update_number(phone_number: str, messages_purchased: int):
        account, created = await Account.get_or_create(
            phone_number=phone_number, defaults={"balance": messages_purchased}
        )
        if not created:
            account.balance += messages_purchased
            await account.save()
        return account

    @staticmethod
    async def decrement_message_count(phone_number: str):
        try:
            account = await Account.get(phone_number=phone_number)
            print("got account", account)
            if account.balance > 0:
                account.balance -= 1
                await account.save()
                return True
            return False
        except DoesNotExist:
            return False

    @staticmethod
    async def get_balance(phone_number: str):
        """
        Retrieves the balance of messages for a specific phone number.

        Args:
            phone_number (str): The phone number to retrieve the balance for.

        Returns:
            int: The number of message credits available.

        Raises:
            DoesNotExist: If no account is found for the provided phone number.
        """
        try:
            account = await Account.get(phone_number=phone_number)
            return account.balance
        except DoesNotExist:
            raise DoesNotExist(f"No account found for the phone number: {phone_number}")
