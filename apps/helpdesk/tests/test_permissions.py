from apps.common.tests.test_permissions import TestPermissions
from config.permissions import UserPermissions
from apps.helpdesk.factories import FaqFactory, ContactMessageFactory
from apps.common.factories import MunicipalityFactory


class TestFaqPermissions(TestPermissions):
    def setUp(self):
        super(TestFaqPermissions, self).setUp()
        self.create_faq = '''
            mutation Mutation($input: FaqCreateInputType!) {
                createFaq(data: $input) {
                    ok
                    errors
                    result {
                      id
                      question
                      answer
                    }
                }
            }
        '''
        self.update_faq = '''
            mutation Mutation($id: ID!, $input:  FaqCreateInputType!) {
                updateFaq(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      question
                      answer
                    }
                }
            }
        '''
        self.delete_faq = '''
            mutation Mutation($id: ID!) {
                deleteFaq(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.faq = FaqFactory.create()
        self.faq_minput = {'question': 'Test question?', 'answer': 'Test answer'}

        super().setUp()

    def test_admin_only_can_create_faq(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_faq, minput=self.faq_minput, okay=True)
        self.assertEqual(content['data']['createFaq']['result']['question'], self.faq_minput['question'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_faq, minput=self.faq_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CREATE_FAQ)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_faq, minput=self.faq_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CREATE_FAQ)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_faq, minput=self.faq_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CREATE_FAQ)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_faq, minput=self.faq_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CREATE_FAQ)
        )

    def test_admin_only_can_update_faqs(self):
        faq = FaqFactory.create()

        # Admin case
        updated_question = 'updated question'
        self.faq_minput['question'] = updated_question

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_faq, minput=self.faq_minput,
            variables={'id': faq.id}, okay=True
        )
        self.assertEqual(content['data']['updateFaq']['result']['question'], updated_question)

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_faq, minput=self.faq_minput, variables={'id': faq.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_FAQ)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_faq, minput=self.faq_minput, variables={'id': faq.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_FAQ)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_faq, minput=self.faq_minput, variables={'id': faq.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_FAQ)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_faq, minput=self.faq_minput, variables={'id': faq.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_FAQ)
        )

    def test_admin_only_can_delete_faq(self):
        # Admin case
        self.force_login(self.super_admin)
        faq = FaqFactory.create()
        self.query_check(self.delete_faq, variables={'id': faq.id}, okay=True)

        faq = FaqFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_faq, variables={'id': faq.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_FAQ)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_faq, variables={'id': faq.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_FAQ)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_faq, variables={'id': faq.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_FAQ)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_faq, variables={'id': faq.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_FAQ)
        )


class TestContactMessagePermissions(TestPermissions):
    def setUp(self):
        super(TestContactMessagePermissions, self).setUp()
        self.create_contact_message = '''
            mutation Mutation($input: ContactMessageInputType!) {
                createContactMessage(data: $input) {
                    ok
                    errors
                    result {
                      id
                      fullName
                      message
                    }
                }
            }
        '''
        self.update_contact_message = '''
            mutation Mutation($id: ID!, $input:  ContactMessageInputType!) {
                updateContactMessage(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      fullName
                      message
                    }
                }
            }
        '''
        self.delete_contact_message = '''
            mutation Mutation($id: ID!) {
                deleteContactMessage(id: $id) {
                    ok
                    errors
                }
            }
        '''
        municipality = MunicipalityFactory.create()
        self.contact_message_minput = {
            'fullName': 'Alex Alex', 'message': 'Test message', 'email': 'alex@gmail.com',
            'municipality': municipality.id,
        }

        super().setUp()

    def test_any_user_can_create_contact_message(self):
        # Anonymous user case
        response = self.query_check(self.create_contact_message, minput=self.contact_message_minput, okay=True)
        self.assertEqual(
            response['data']['createContactMessage']['result']['fullName'],
            self.contact_message_minput['fullName']
        )
        # Admin case
        self.force_login(self.super_admin)
        response = self.query_check(self.create_contact_message, minput=self.contact_message_minput, okay=True)
        self.assertEqual(
            response['data']['createContactMessage']['result']['fullName'],
            self.contact_message_minput['fullName']
        )

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_contact_message, minput=self.contact_message_minput, okay=True)
        self.assertEqual(
            response['data']['createContactMessage']['result']['fullName'],
            self.contact_message_minput['fullName']
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_contact_message, minput=self.contact_message_minput, okay=True)
        self.assertEqual(
            response['data']['createContactMessage']['result']['fullName'],
            self.contact_message_minput['fullName']
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_contact_message, minput=self.contact_message_minput, okay=True)
        self.assertEqual(
            response['data']['createContactMessage']['result']['fullName'],
            self.contact_message_minput['fullName']
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_contact_message, minput=self.contact_message_minput, okay=True)
        self.assertEqual(
            response['data']['createContactMessage']['result']['fullName'],
            self.contact_message_minput['fullName']
        )

    def test_admin_only_update_contact_message(self):
        contact_message = ContactMessageFactory.create()

        # Admin case
        updated_name = 'Sita joshi'
        self.contact_message_minput['fullName'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_contact_message, minput=self.contact_message_minput,
            variables={'id': contact_message.id}, okay=True
        )
        self.assertEqual(content['data']['updateContactMessage']['result']['fullName'], updated_name)

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_contact_message, minput=self.contact_message_minput, variables={'id': contact_message.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_CONTACT_MESSAGE)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_contact_message, minput=self.contact_message_minput, variables={'id': contact_message.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_CONTACT_MESSAGE)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_contact_message, minput=self.contact_message_minput, variables={'id': contact_message.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_CONTACT_MESSAGE)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_contact_message, minput=self.contact_message_minput, variables={'id': contact_message.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.UPDATE_CONTACT_MESSAGE)
        )

    def test_admin_only_delete_contact_message(self):
        # Admin case
        self.force_login(self.super_admin)
        contact_message = ContactMessageFactory.create()
        self.query_check(self.delete_contact_message, variables={'id': contact_message.id}, okay=True)

        contact_message = ContactMessageFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_contact_message, variables={'id': contact_message.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_CONTACT_MESSAGE)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_contact_message, variables={'id': contact_message.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_CONTACT_MESSAGE)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_contact_message, variables={'id': contact_message.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_CONTACT_MESSAGE)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_contact_message, variables={'id': contact_message.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.DELETE_CONTACT_MESSAGE)
        )
