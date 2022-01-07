from django.core.management.base import BaseCommand
import json
from apps.common.models import Province, District, Municipality


class Command(BaseCommand):
    help = 'Init province, district, municipalities of nepal'

    def handle(self, *args, **options):
        # Bulk create provinces
        province_file = open('seed/province.json')
        provinces = json.load(province_file)
        provinces_created = Province.objects.bulk_create(
            [
                Province(
                    pk=province['id'],
                    name_en=province['name_en'],
                    name_ne=province['name_ne'],
                )
                for province in provinces
            ]
        )
        self.stdout.write(self.style.SUCCESS(f'{len(provinces_created)} provinces created.'))

        # Bulk create district
        district_file = open('seed/district.json')
        districts = json.load(district_file)
        districts_created = District.objects.bulk_create(
            [
                District(
                    pk=district['id'],
                    name_en=district['name_en'],
                    name_ne=district['name_ne'],
                    province_id=district['province_id']
                )
                for district in districts
            ]
        )
        self.stdout.write(self.style.SUCCESS(f'{len(districts_created)} districts created.'))

        # Bulk create municipalities
        municipality_file = open('seed/municipality.json')
        municipalities = json.load(municipality_file)
        municipalities_created = Municipality.objects.bulk_create(
            [
                Municipality(
                    pk=municipality['id'],
                    name_en=municipality['name_en'],
                    name_ne=municipality['name_ne'],
                    province_id=municipality['province_id'],
                    district_id=municipality['district_id']
                )
                for municipality in municipalities
            ]
        )
        self.stdout.write(self.style.SUCCESS(f'{len(municipalities_created)} municipalities created.'))
