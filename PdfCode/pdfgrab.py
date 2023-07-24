import Urlsnatcher
import pdfmaker
from cik import get_CIK_num

ticker_cik_dict = get_CIK_num()
for tick, cik in list(ticker_cik_dict.items())[0:600]:
    # do something with ticker and cik
    user_data = {'tick': tick, 'form': '10-K', 'range': ('15', '22')}
    urls = Urlsnatcher.get_url(user_data['tick'], user_data['form'], user_data['range'])
    name = pdfmaker.make_pdf(urls, user_data)