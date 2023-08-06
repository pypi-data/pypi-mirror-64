from vcr_unittest import VCRTestCase

from corona_chan_gob_mx import get_today_cases
from corona_chan_gob_mx.scraper import list_of_pdf


class Test_get_today_cases( VCRTestCase ):
    def test_should_combine_both_list_in_one( self ):
        cases = get_today_cases()
        tables = list_of_pdf.get().native
        self.assertEqual(
            len( cases ),
            len( tables[0].get().native + tables[1].get().native ) )
