"""Invitations tests."""

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework import status

# Model
from cride.circles.models import Circle, Invitation, Membership
from cride.users.models import User, Profile
from rest_framework.authtoken.models import Token


class InvitationsManagerTestCase(TestCase):
    """Invitations manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Manuel',
            last_name='Pita',
            email='mpita1984@gmail.com',
            username='mpita',
            password='admin123'
        )
        self.circle = Circle.objects.create(
            name='Test Django',
            slug_name='test_django',
            about='data of test django',
            verified=True
        )

    def test_code_generation(self):
        """Random codes should be generated automatically."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        code = 'helloword'
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """If given code is not unique, a new one must be generated."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        ).code

        # Create another invitation with the past code
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )

        self.assertNotEqual(code, invitation.code

        )


class MemberInvitationsAPITestCase(APITestCase):
    """Member invitation API test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Manuel',
            last_name='Pita',
            email='mpita1984@gmail.com',
            username='mpita',
            password='admin123'
        )
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.circle = Circle.objects.create(
            name='Test Django',
            slug_name='test_django',
            about='data of test django',
            verified=True
        )
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

        #Url
        self.url = "/circles/{}/members/{}/invitations/".format(
            self.circle.slug_name,
            self.user.username
        )

    def test_success(self):
        """Verify request succeed."""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitation are generated if none exist previously."""

        # Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(), 0)

        # Call member invitations
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verify new invitations were created
        invitations = Invitation.objects.filter(
            issued_by=self.user
        )
        self.assertEqual(
            invitations.count(),
            self.membership.remaining_invitations
        )
        for inv in invitations:
            self.assertIn(inv.code, request.data['invitations'])
