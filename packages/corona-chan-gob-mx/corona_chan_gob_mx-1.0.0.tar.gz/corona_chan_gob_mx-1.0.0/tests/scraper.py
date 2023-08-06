from chibi_requests import Chibi_url
from vcr_unittest import VCRTestCase

from corona_chan_gob_mx.scraper import list_of_pdf, pdf_to_dicts
from chibi.file.temp import Chibi_temp_path


class Test_scraper( VCRTestCase ):
    def test_the_result_should_be_a_list_of_chibi_urls( self ):
        result = list_of_pdf.get()
        self.assertTrue( result.native )
        for link in result.native:
            self.assertIsInstance( link, Chibi_url )

    def test_all_the_case_should_start_with_tabla_casos( self ):
        result = list_of_pdf.get()
        self.assertTrue( result.native )
        for link in result.native:
            self.assertTrue( link.base_name.startswith( 'Tabla_casos' ) )

    def test_should_return_the_table_of_the_pdf( self ):
        result = list_of_pdf.get()
        self.assertTrue( result.native )
        for link in result.native:
            temp_folder = Chibi_temp_path()
            pdf = link.download( temp_folder )
            table = pdf_to_dicts( pdf )
            self.assertIsInstance( table, list )
            for t in table:
                self.assertIsInstance( t, dict )
                self.assertIn( 'number_case', t )
                self.assertIn( 'age', t )
                self.assertIn( 'state', t )
                self.assertIn( 'symptom_start_date', t )
                self.assertIn( 'arrive_date_to_mexico', t )
                self.assertIn( 'status', t )
                self.assertIn( 'arrive_from', t )
                self.assertIn( 'sex', t )

    def test_pdf_link_should_use_the_get_for_get_data( self ):
        links = list_of_pdf.get()
        for link in links.native:
            response = link.get()
            self.assertIsInstance( response.native, list )
            for t in response.native:
                self.assertIsInstance( t, dict )
                self.assertIn( 'number_case', t )
                self.assertIn( 'age', t )
                self.assertIn( 'state', t )
                self.assertIn( 'symptom_start_date', t )
                self.assertIn( 'arrive_date_to_mexico', t )
                self.assertIn( 'status', t )
                self.assertIn( 'arrive_from', t )
                self.assertIn( 'sex', t )
