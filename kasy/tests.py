import datetime
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Kasa, Model_kasy, Podatnik, Producent_kasy, Urzad_skarbowy
from .utils import SmsApiError


class KasaSmsViewTests(TestCase):
    def setUp(self):
        producent = Producent_kasy.objects.create(
            nazwa='Producent', ulica='Testowa', nr_domu='1',
            kod_pocztowy='00-001', miasto='Warszawa',
        )
        model = Model_kasy.objects.create(
            nazwa='Model testowy', producent=producent,
        )
        urzad = Urzad_skarbowy.objects.create(
            nazwa='US', ulica='Testowa', nr_domu='1',
            kod_pocztowy='00-001', miasto='Warszawa', nr_urzedu=1,
        )
        podatnik = Podatnik.objects.create(
            nazwa='Podatnik', kod_pocztowy='00-001', miasto='Warszawa',
            ulica='Testowa', nr_domu='1', nip='1234567890',
            wojewodzctwo='mazowieckie', gmina='Warszawa',
            poczta='Warszawa', telefon='500600700', urzad_skarbowy=urzad,
        )
        self.kasa = Kasa.objects.create(
            model_kasy=model, nr_unikatowy='ABC123', nr_fabryczny='FAB123',
            podatnik=podatnik, data_fisk=datetime.date(2025, 9, 1),
            nastepny_przeg=datetime.date(2026, 9, 1),
        )

    @patch('kasy.views.send_sms')
    @override_settings(SMSAPI_MESSAGE_TEMPLATE='Przeglad: {date}')
    def test_sms_is_marked_only_after_successful_send(self, send_sms_mock):
        send_sms_mock.return_value = {
            'count': 1,
            'list': [{'id': 'test-id', 'status': 'QUEUE'}],
        }
        response = self.client.post(
            reverse('kasa_sms', args=[self.kasa.pk]), follow=True,
        )

        self.assertRedirects(response, reverse('home'))
        self.kasa.refresh_from_db()
        self.assertTrue(self.kasa.sms)
        self.assertEqual(self.kasa.data_sms, datetime.date.today())
        send_sms_mock.assert_called_once_with('500600700', 'Przeglad: 01.09.2026')
        self.assertContains(response, 'SMSAPI: QUEUE (ID: test-id)')

    @patch('kasy.views.send_sms', side_effect=SmsApiError('awaria'))
    def test_sms_is_not_marked_when_api_fails(self, send_sms_mock):
        response = self.client.post(reverse('kasa_sms', args=[self.kasa.pk]))

        self.assertRedirects(response, reverse('home'))
        self.kasa.refresh_from_db()
        self.assertFalse(self.kasa.sms)
        self.assertIsNone(self.kasa.data_sms)

    def test_sms_endpoint_rejects_get(self):
        self.assertEqual(
            self.client.get(reverse('kasa_sms', args=[self.kasa.pk])).status_code,
            405,
        )
