from .flipkart_cat import cat_list


def main(
        product='https://www.flipkart.com/lois-caron-lcs-8075-blue-dial-day-date-functioning-analog-watch-men/p/itmf86ur97ygfgtv?pid=WATF86RM6G9QCGYR&lid=LSTWATF86RM6G9QCGYRIWLX1J&marketplace=FLIPKART&srno=b_1_1&otracker=hp_omu_Deals%2Bof%2Bthe%2BDay_5_2.dealCard.OMU_TQQXT6S3UKKT_2&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Deals%2Bof%2Bthe%2BDay_NA_dealCard_cc_5_NA_view-all_2&fm=neo%2Fmerchandising&iid=0304cd85-2938-49c6-85c6-7296424958c0.WATF86RM6G9QCGYR.SEARCH&ppt=browse&ppn=browse&ssid=mfgzdss3e8tgk64g1559969538836'):
    # product = input("Enter product name:")
    # product = "phones"
    return cat_list(product)

# if __name__ == '__main__':
#     main()
