from utils.graphene.tests import GraphQLTestCase

from apps.user.factories import UserFactory
from apps.payment.factories import PaymentFactory
from apps.user.models import User
from apps.payment.filter_set import PaymentFilterSet
from apps.payment.models import Payment


class TestPaymentQuery(GraphQLTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.filter_class = PaymentFilterSet

    def test_payment_query(self):
        query = '''
            query MyQuery {
              moderatorQuery {
                payments (ordering: "id") {
                    totalCount
                    results {
                        amount
                        createdAt
                        id
                        paymentType
                        status
                        transactionType
                    }
                  }
                }
            }
        '''
        other_user = UserFactory.create()
        moderator_user = UserFactory.create(user_type=User.UserType.MODERATOR)
        PaymentFactory.create()
        PaymentFactory.create()
        PaymentFactory.create()

        # without login
        self.query_check(query, assert_for_error=True)

        # login with different user
        self.force_login(other_user)

        content = self.query_check(query)
        self.assertEqual(content['data']['moderatorQuery'], None)

        # login with moderator user
        self.force_login(moderator_user)

        content = self.query_check(query)
        self.assertEqual(content['data']['moderatorQuery']['payments']['totalCount'], 3, content)

    def test_payment_filter(self):
        payment_1 = PaymentFactory.create(
            payment_type=Payment.PaymentType.CASH,
            transaction_type=Payment.TransactionType.CREDIT,
            status=Payment.Status.PENDING,
        )
        payment_2 = PaymentFactory.create(
            payment_type=Payment.PaymentType.CASH,
            transaction_type=Payment.TransactionType.CREDIT,
            status=Payment.Status.PENDING,
        )
        payment_3 = PaymentFactory.create(
            payment_type=Payment.PaymentType.CHEQUE,
            transaction_type=Payment.TransactionType.CREDIT,
            status=Payment.Status.CANCELLED,
        )
        payment_4 = PaymentFactory.create(
            payment_type=Payment.PaymentType.CHEQUE,
            transaction_type=Payment.TransactionType.DEBIT,
            status=Payment.Status.PENDING
        )
        payment_5 = PaymentFactory.create(
            payment_type=Payment.PaymentType.CASH,
            transaction_type=Payment.TransactionType.CREDIT,
            status=Payment.Status.VERIFIED,
        )

        # filter status
        obtained = self.filter_class(data=dict(status=Payment.Status.PENDING.value)).qs
        expected = [payment_1, payment_2, payment_4]
        self.assertQuerySetIdEqual(
            expected,
            obtained
        )

        # filter transaction_type
        obtained = self.filter_class(data=dict(transaction_type=Payment.TransactionType.CREDIT.value)).qs
        expected = [payment_1, payment_2, payment_3, payment_5]
        self.assertQuerySetIdEqual(
            expected,
            obtained
        )

        # filter payment_type
        obtained = self.filter_class(data=dict(payment_type=Payment.PaymentType.CHEQUE.value)).qs
        expected = [payment_3, payment_4]
        self.assertQuerySetIdEqual(
            expected,
            obtained
        )

    def test_payment_mutation(self):
        create_mutation = '''
            mutation MyMutation ($input: PaymentInputType!) {
                moderatorMutation {
                    createPayment(data: $input) {
                        errors
                        ok
                        result {
                            amount
                            createdAt
                            createdBy {
                                id
                            }
                            modifiedBy {
                                id
                            }
                            paidBy {
                                id
                            }
                            id
                            paymentType
                            status
                            transactionType
                        }
                    }
                }
            }
        '''

        update_mutation = '''
            mutation MyMutation ($id: ID!, $input: PaymentInputType!) {
                moderatorMutation {
                    updatePayment(id: $id, data: $input) {
                        errors
                        ok
                        result {
                            amount
                            createdAt
                            createdBy {
                                id
                            }
                            modifiedBy {
                                id
                            }
                            paidBy {
                                id
                            }
                            id
                            paymentType
                            status
                            transactionType
                        }
                    }
                }
            }
        '''

        other_user = UserFactory.create()
        moderator_user = UserFactory.create(user_type=User.UserType.MODERATOR)
        self.input = dict(
            amount=123.72,
            paidBy=other_user.pk,
            paymentType=self.genum(Payment.PaymentType.CASH),
            transactionType=self.genum(Payment.TransactionType.CREDIT),
            status=self.genum(Payment.Status.PENDING)
        )

        # without login
        self.query_check(
            create_mutation,
            input_data=self.input,
            assert_for_error=True
        )

        # login with different user
        self.force_login(moderator_user)

        response = self.query(
            create_mutation,
            input_data=self.input
        )
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertTrue(content['data']['moderatorMutation']['createPayment']['ok'], content)
        self.assertTrue(content['data']['moderatorMutation']['createPayment']['result']['paidBy']['id'], other_user.id)
        response_id = content['data']['moderatorMutation']['createPayment']['result']['id']

        minput = dict(
            amount=123.72,
            paidBy=other_user.pk,
            paymentType=self.genum(Payment.PaymentType.CHEQUE),
            transactionType=self.genum(Payment.TransactionType.DEBIT),
            status=self.genum(Payment.Status.CANCELLED),
        )

        def _query_check(**kwargs):
            return self.query_check(
                update_mutation,
                minput=minput,
                variables={'id': response_id},
                **kwargs
            )
        _query_check(assert_for_error=False)
        content = _query_check()
        self.assertTrue(content['data']['moderatorMutation']['updatePayment']['ok'], content)
        self.assertEqual(
            content['data']['moderatorMutation']['updatePayment']['result']['status'],
            self.genum(Payment.Status.CANCELLED)
        )
