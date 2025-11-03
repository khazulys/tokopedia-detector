import requests
import json
import time
import random
from typing import Dict, Optional
from ..utils import HeaderGenerator

class APIFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.header_gen = HeaderGenerator()
    
    def fetch_product_info(self, product_url: str) -> Optional[Dict]:
        url = "https://gql.tokopedia.com/graphql/productrevGetMiniProductInfo"
        payload = [{
            "operationName": "productrevGetMiniProductInfo",
            "variables": {
                "productURL": product_url,
                "userLocation": {
                    "addressID": "",
                    "districtID": "2274",
                    "postalCode": "",
                    "latlon": ""
                }
            },
            "query": "query productrevGetMiniProductInfo($productURL: String!, $userLocation: productrevUserLocation) {\n  productrevGetMiniProductInfo(\n    productID: \"\"\n    productURL: $productURL\n    userLocation: $userLocation\n  ) {\n    product {\n      id\n      name\n      thumbnailURL\n      price\n      status\n      stock\n      priceFmt\n      __typename\n    }\n    campaign {\n      isActive\n      discountPercentage\n      discountedPrice\n      __typename\n    }\n    __typename\n  }\n}"
        }]
        
        headers = self.header_gen.generate(product_url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(random.uniform(0.5, 1.5))
        
        if response.status_code == 200:
            return response.json()[0]['data']['productrevGetMiniProductInfo']
        return None
    
    def fetch_reviews(self, product_url: str, product_id: Optional[str] = None, 
                     page: int = 1, limit: int = 20, sort_by: str = "informative_score desc") -> Optional[Dict]:
        url = "https://gql.tokopedia.com/graphql/productReviewList"
        payload = [{
            "operationName": "productReviewList",
            "variables": {
                "productURL": product_url,
                "page": page,
                "limit": limit,
                "sortBy": sort_by,
                "filterBy": "",
                "opt": ""
            },
            "query": "query productReviewList($productURL: String!, $page: Int!, $limit: Int!, $sortBy: String, $filterBy: String, $opt: String) {\n  productrevGetProductReviewList(\n    productID: \"\"\n    productURL: $productURL\n    page: $page\n    limit: $limit\n    sortBy: $sortBy\n    filterBy: $filterBy\n    opt: $opt\n  ) {\n    productID\n    list {\n      id: feedbackID\n      variantName\n      message\n      productRating\n      reviewCreateTime\n      reviewCreateTimestamp\n      isReportable\n      isAnonymous\n      videoAttachments {\n        attachmentID\n        videoUrl\n        __typename\n      }\n      imageAttachments {\n        attachmentID\n        imageThumbnailUrl\n        imageUrl\n        __typename\n      }\n      reviewResponse {\n        message\n        createTime\n        __typename\n      }\n      user {\n        userID\n        fullName\n        image\n        url\n        label\n        __typename\n      }\n      likeDislike {\n        totalLike\n        likeStatus\n        __typename\n      }\n      stats {\n        key\n        formatted\n        count\n        __typename\n      }\n      badRatingReasonFmt\n      __typename\n    }\n    shop {\n      shopID\n      name\n      url\n      image\n      __typename\n    }\n    variantFilter {\n      isUnavailable\n      ticker\n      __typename\n    }\n    hasNext\n    __typename\n  }\n}"
        }]
        
        headers = self.header_gen.generate(product_url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(random.uniform(0.5, 1.5))
        
        if response.status_code == 200:
            return response.json()[0]['data']['productrevGetProductReviewList']
        return None
    
    def fetch_rating_and_topics(self, product_url: str) -> Optional[Dict]:
        url = "https://gql.tokopedia.com/graphql/productrevGetProductRatingAndTopics"
        
        payload = [{
            "operationName": "productrevGetProductRatingAndTopics",
            "variables": {
                "productURL": product_url,
                "filterBy": "",
                "pageSource": "filter"
            },
            "query": "query productrevGetProductRatingAndTopics($productURL: String!, $filterBy: String, $pageSource: String) {\n  productrevGetProductRatingAndTopics(\n    productURL: $productURL\n    productID: \"\"\n    filterBy: $filterBy\n    pageSource: $pageSource\n  ) {\n    productID\n    rating {\n      positivePercentageFmt\n      ratingScore\n      totalRating\n      totalRatingWithImage\n      totalRatingTextAndImage\n      detail {\n        rate\n        totalReviews\n        formattedTotalReviews\n        percentageFloat\n        __typename\n      }\n      __typename\n    }\n    topics {\n      rating\n      ratingFmt\n      formatted\n      key\n      reviewCount\n      reviewCountFmt\n      show\n      __typename\n    }\n    keywords {\n      text\n      count\n      __typename\n    }\n    availableFilters {\n      withAttachment\n      rating\n      topics\n      helpfulness\n      variant\n      __typename\n    }\n    variantsData {\n      name\n      option {\n        id\n        name\n        image\n        __typename\n      }\n      __typename\n    }\n    pairedVariantsData {\n      optionIDs\n      __typename\n    }\n    layout {\n      backgroundColor\n      reviewSourceIconUrl\n      reviewSourceText\n      __typename\n    }\n    __typename\n  }\n}"
        }]
        
        headers = self.header_gen.generate(product_url)
        headers['x-theme'] = "default"
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(random.uniform(0.5, 1.5))
        
        if response.status_code == 200:
            return response.json()[0]['data']['productrevGetProductRatingAndTopics']
        return None
    
    def search_products(self, query: str, page: int = 1, rows: int = 8) -> Optional[Dict]:
        url = "https://gql.tokopedia.com/graphql/SearchProductV5Query"
        
        search_param = f"device=mobile&enable_lite_deduplication=true&enter_method=normal_search&l_name=sre&navsource=home&ob=23&page={page}&q={query}&rows={rows}&source=search&srp_component_id=02.01.00.00&unique_id={random.randint(1000000000000000000, 9999999999999999999)}&use_page=true&user_cityId=176&user_districtId=2274&warehouses="
        
        payload = [{
            "operationName": "SearchProductV5Query",
            "variables": {
                "searchProductV5Param": search_param
            },
            "query": "query SearchProductV5Query($searchProductV5Param: String!) {\n  searchProductV5(params: $searchProductV5Param) {\n    header {\n      totalData\n      responseCode\n      keywordProcess\n      keywordIntention\n      componentID\n      isQuerySafe\n      additionalParams\n      backendFilters\n      backendFiltersToggle\n      meta {\n        dynamicFields\n        __typename\n      }\n      __typename\n    }\n    data {\n      totalDataText\n      banner {\n        position\n        text\n        url\n        imageURL\n        componentID\n        trackingOption\n        __typename\n      }\n      redirection {\n        url\n        applink\n        __typename\n      }\n      related {\n        relatedKeyword\n        position\n        trackingOption\n        otherRelated {\n          keyword\n          url\n          applink\n          componentID\n          products {\n            oldId: id\n            id: id_str_auto_\n            name\n            url\n            applink\n            mediaURL {\n              image\n              __typename\n            }\n            shop {\n              oldId: id\n              id: id_str_auto_\n              name\n              city\n              tier\n              __typename\n            }\n            badge {\n              id\n              title\n              url\n              __typename\n            }\n            price {\n              text\n              number\n              __typename\n            }\n            freeShipping {\n              url\n              __typename\n            }\n            labelGroups {\n              id\n              position\n              title\n              type\n              url\n              styles {\n                key\n                value\n                __typename\n              }\n              __typename\n            }\n            rating\n            wishlist\n            ads {\n              id\n              productClickURL\n              productViewURL\n              productWishlistURL\n              tag\n              __typename\n            }\n            meta {\n              oldWarehouseID: warehouseID\n              warehouseID: warehouseID_str_auto_\n              componentID\n              oldParentID: parentID\n              parentID: parentID_str_auto_\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        query\n        text\n        componentID\n        trackingOption\n        __typename\n      }\n      shopWidget {\n        headline {\n          badge {\n            id\n            title\n            url\n            __typename\n          }\n          shop {\n            id\n            ttsSellerID\n            location\n            City\n            name\n            ratingScore\n            imageShop {\n              sURL\n              __typename\n            }\n            products {\n              id\n              id_str_auto_\n              ttsProductID\n              name\n              url\n              rating\n              mediaURL {\n                image\n                image300\n                videoCustom\n                __typename\n              }\n              shop {\n                oldId: id\n                id: id_str_auto_\n                ttsSellerID\n                name\n                city\n                __typename\n              }\n              price {\n                text\n                number\n                range\n                discountPercentage\n                original\n                __typename\n              }\n              labelGroups {\n                id\n                position\n                title\n                type\n                url\n                styles {\n                  key\n                  value\n                  __typename\n                }\n                __typename\n              }\n              meta {\n                oldParentID: parentID\n                parentID: parentID_str_auto_\n                isPortrait\n                oldWarehouseID: warehouseID\n                warehouseID: warehouseID_str_auto_\n                __typename\n              }\n              stock {\n                ttsSKUID\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        meta {\n          redirect\n          __typename\n        }\n        __typename\n      }\n      ticker {\n        id\n        text\n        query\n        applink\n        componentID\n        trackingOption\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      products {\n        oldId: id\n        id: id_str_auto_\n        ttsProductID\n        name\n        url\n        applink\n        mediaURL {\n          image\n          image300\n          videoCustom\n          __typename\n        }\n        shop {\n          oldId: id\n          id: id_str_auto_\n          ttsSellerID\n          name\n          url\n          city\n          tier\n          __typename\n        }\n        stock {\n          ttsSKUID\n          __typename\n        }\n        badge {\n          id\n          title\n          url\n          __typename\n        }\n        price {\n          text\n          number\n          range\n          original\n          discountPercentage\n          __typename\n        }\n        freeShipping {\n          url\n          __typename\n        }\n        labelGroups {\n          id\n          position\n          title\n          type\n          url\n          styles {\n            key\n            value\n            __typename\n          }\n          __typename\n        }\n        labelGroupsVariant {\n          title\n          type\n          typeVariant\n          hexColor\n          __typename\n        }\n        category {\n          oldId: id\n          id: id_str_auto_\n          name\n          breadcrumb\n          gaKey\n          __typename\n        }\n        rating\n        wishlist\n        ads {\n          id\n          productClickURL\n          productViewURL\n          productWishlistURL\n          tag\n          __typename\n        }\n        meta {\n          oldParentID: parentID\n          parentID: parentID_str_auto_\n          oldWarehouseID: warehouseID\n          warehouseID: warehouseID_str_auto_\n          isImageBlurred\n          isPortrait\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
        }]
        
        headers = self.header_gen.generate()
        headers.update({
            'x-dark-mode': "false",
            'x-device': "mobile",
            'bd-web-id': str(random.randint(7000000000000000000, 7999999999999999999))
        })
        
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(random.uniform(0.5, 1.5))
        
        if response.status_code == 200:
            return response.json()[0]['data']['searchProductV5']
        return None
    
    def fetch_shop_detail(self, shop_domain: str) -> Optional[Dict]:
        url = "https://gql.tokopedia.com/graphql/ShopInfoCoreQuery"
        
        payload = [{
            "operationName": "ShopInfoCoreQuery",
            "variables": {
                "shopIDs": [0],
                "domain": shop_domain,
                "fields": [
                    "allow_manage", "assets", "core", "create_info", "favorite",
                    "location", "other-goldos", "other-shiploc", "status",
                    "shipment", "shop-snippet", "goapotik", "fs_type",
                    "tts_integration_completed"
                ]
            },
            "query": "query ShopInfoCoreQuery($shopIDs: [Int!]!, $fields: [String!]!, $domain: String) {\n  shopInfoByID(\n    input: {shopIDs: $shopIDs, fields: $fields, domain: $domain, source: \"gql-shoppage-lite\"}\n  ) {\n    result {\n      favoriteData {\n        totalFavorite\n        alreadyFavorited\n        __typename\n      }\n      goldOS {\n        isGold\n        isGoldBadge\n        isOfficial\n        badge\n        __typename\n      }\n      location\n      isAllowManage\n      shippingLoc {\n        districtName\n        cityName\n        __typename\n      }\n      shopAssets {\n        avatar\n        cover\n        __typename\n      }\n      shopCore {\n        description\n        domain\n        shopID\n        name\n        shopScore\n        tagLine\n        url\n        __typename\n      }\n      statusInfo {\n        shopStatus\n        statusMessage\n        statusTitle\n        tickerType\n        __typename\n      }\n      createInfo {\n        shopCreated\n        epochShopCreated\n        openSince\n        __typename\n      }\n      bbInfo {\n        bbName\n        bbDesc\n        bbNameEN\n        bbDescEN\n        __typename\n      }\n      shipmentInfo {\n        isAvailable\n        code\n        image\n        name\n        product {\n          isAvailable\n          productName\n          shipProdID\n          uiHidden\n          __typename\n        }\n        isPickup\n        maxAddFee\n        awbStatus\n        __typename\n      }\n      shopSnippetURL\n      customSEO {\n        title\n        description\n        bottomContent\n        __typename\n      }\n      isQA\n      isGoApotik\n      epharmacyInfo {\n        siaNumber\n        sipaNumber\n        apj\n        __typename\n      }\n      partnerInfo {\n        fsType\n        __typename\n      }\n      ttsIntegrationCompletedData {\n        ttsSellerID\n        __typename\n      }\n      __typename\n    }\n    error {\n      message\n      __typename\n    }\n    __typename\n  }\n}"
        }]
        
        headers = self.header_gen.generate()
        headers['x-device'] = "tokopedia-lite"
        
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(random.uniform(0.5, 1.5))
        
        if response.status_code == 200:
            data = response.json()[0]['data']['shopInfoByID']
            if data and data.get('result') and len(data['result']) > 0:
                return data['result'][0]
        return None
    
    def fetch_shop_rating(self, shop_id: str) -> Optional[Dict]:
        url = "https://gql.tokopedia.com/graphql/ShopPageGetRating"
        
        payload = [{
            "operationName": "ShopPageGetRating",
            "variables": {
                "shopId": shop_id
            },
            "query": "query ShopPageGetRating($shopId: String!) {\n  productrevGetShopRating(shopID: $shopId) {\n    detail {\n      formattedTotalReviews\n      rate\n      percentage\n      percentageFloat\n      totalReviews\n      __typename\n    }\n    ratingScore\n    totalRating\n    __typename\n  }\n}"
        }]
        
        headers = self.header_gen.generate()
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(random.uniform(0.3, 0.8))
        
        if response.status_code == 200:
            data = response.json()[0]['data']
            if data and data.get('productrevGetShopRating'):
                return data['productrevGetShopRating']
        return None
    
    def fetch_shop_products(self, shop_id: str, page: int = 1, per_page: int = 10) -> Optional[Dict]:
        url = "https://gql.tokopedia.com/graphql/GetShopProduct"
        
        payload = [{
            "operationName": "GetShopProduct",
            "variables": {
                "shopID": shop_id,
                "page": page,
                "perPage": per_page,
                "fkeyword": "",
                "fmenu": "all",
                "sort": 2,
                "user_districtId": "2274",
                "user_cityId": "176",
                "user_lat": "0",
                "user_long": "0",
                "rating": None,
                "pmin": None,
                "pmax": None,
                "fcategory": None,
                "source": "shop"
            },
            "query": "query GetShopProduct($shopID: String!, $page: Int, $perPage: Int, $fkeyword: String, $fmenu: String, $sort: Int, $rating: String, $pmin: Int, $pmax: Int, $user_districtId: String, $user_cityId: String, $user_lat: String, $user_long: String, $fcategory: Int, $source: String, $extraParam: String) {\n  GetShopProduct(\n    shopID: $shopID\n    source: $source\n    filter: {page: $page, perPage: $perPage, fkeyword: $fkeyword, fmenu: $fmenu, sort: $sort, rating: $rating, pmin: $pmin, pmax: $pmax, user_districtId: $user_districtId, user_cityId: $user_cityId, user_lat: $user_lat, user_long: $user_long, fcategory: $fcategory, usecase: \"ace_get_shop_product_v2\", extraParam: $extraParam}\n  ) {\n    status\n    errors\n    links {\n      self\n      next\n      prev\n      __typename\n    }\n    suggestion {\n      text\n      query\n      response_code\n      keyword_process\n      __typename\n    }\n    totalData\n    additionalParams\n    data {\n      product_id\n      tts_product_id\n      tts_sku_id\n      parent_id\n      name\n      product_url\n      status\n      stock\n      sold\n      hasVariant\n      show_stockbar\n      price {\n        text_idr\n        __typename\n      }\n      flags {\n        id: product_id\n        isFeatured\n        isPreorder\n        isWishlist\n        isWholesale\n        isFreereturn\n        mustInsurance\n        supportFreereturn\n        withStock\n        isSold\n        __typename\n      }\n      label {\n        icon\n        color_hex\n        color_rgb\n        content\n        __typename\n      }\n      label_groups {\n        position\n        title\n        type\n        url\n        styles {\n          key\n          value\n          __typename\n        }\n        __typename\n      }\n      badge {\n        title\n        image_url\n        __typename\n      }\n      stats {\n        reviewCount\n        rating\n        averageRating\n        __typename\n      }\n      primary_image {\n        thumbnail\n        __typename\n      }\n      cashback {\n        cashback\n        cashback_amount\n        __typename\n      }\n      campaign {\n        hide_gimmick\n        is_active\n        is_upcoming\n        original_price\n        original_price_fmt\n        discounted_percentage\n        discounted_price_fmt\n        stock_sold_percentage\n        __typename\n      }\n      freeOngkir {\n        isActive\n        imgURL\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
        }]
        
        headers = self.header_gen.generate()
        headers['x-device'] = "tokopedia-lite"
        
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(random.uniform(0.3, 0.8))
        
        if response.status_code == 200:
            data = response.json()[0]['data']
            if data and data.get('GetShopProduct'):
                return data['GetShopProduct']
        return None
