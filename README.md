# school_meal_discount
# 壹、動機
在一次吃學餐的過程中，我們發現學生餐廳的人流量雖然不大，卻能明顯感受到點餐的壅塞情況，結合所學知識提出此專案。首先我們致力於為學生餐廳帶來一個全新的行銷策略，透過優惠活動的方式吸引更多學生顧客。這個專案的核心理念在於提供學生們更多的優惠和價值，同時促進學生餐廳的營業額增長。 其次，我們認為優惠活動對學生餐廳是有必要的存在，因此著手進行此專案。透過提供各種優惠活動，我們期望能夠吸引更多學生顧客，增加他們的消費頻率和平均消費額，從而提升整體營業收益。同時，我們還注意到尖峰時段點餐流程的不便之處，因此加入線上付款功能，以提升點餐的便利性和效率。透過優惠活動，我們也能夠增強餐廳的品牌形象，建立良好的口碑，吸引更多新客戶的加入。 至於該如何做到則是因為此系統能夠利用資料庫的力量和系統化的方式讓銷貨流程電子化、記錄業者銷貨紀錄，並讓業者的商品內容可以在APP和網頁上顯示給一般使用者來做選擇及預購。積分、抽獎和優惠券也可以吸引學生以更便宜的價格來消費學餐並讓學餐業者的收益增加。而對系統擁有者的我們而言，可以和業者收取使用系統的抽成來獲取收益。 
# 貳、目的
整合各店家菜單並增加線上付款功能，使點餐更便捷，透過優惠活動的方式吸引更多學生顧客消費的同時減輕學生飲食方面的負擔並增加學餐的銷售額。此專案將注重整合各店家的菜單，並新增線上付款功能，以提升點餐的便利性和效率。總結來說，我們想製作的系統是一個能夠做到讓學生省錢、業者賺取更多的收益、系統擁有者也可以獲得收益的APP，使業者在獲取更多利益的同時，長期向學校租賃店面並升級自身的產品，讓學生有更高的意願來學餐消費，藉此達到永續經營。
# 參、功能說明與設計
整合各店家菜單並增加線上付款功能，使點餐更便捷，透過優惠活動的方式吸引更多學生顧客消費的同時減輕學生飲食方面的負擔並增加學餐的銷售額。此專案將注重整合各店家的菜單，並新增線上付款功能，以提升點餐的便利性和效率。
一、	會員管理：透過LineBot進行會員註冊，用戶填寫個人資料並建立個人帳戶，建立帳戶後依據身分組和權限的不同會有不同的功能，一般使用者可以利用購買學餐來獲取積分和抽獎機會並可以利用積分來換取優惠券，業者則可以利用系統來確認營業額、優惠券數量並可即時確認庫存狀況。
二、	積分制度：系統管理者設置積分制度，一般用戶可以透過消費學餐、分享等方式獲取積分，積分可用於換取優惠券和票券抽獎。
三、	優惠資訊：系統管理者與業者溝通後建立各種優惠券供一般用戶兌換，用戶可利用消費學餐或邀請好友所獲得的積分來換取不同程度上的折扣。
四、	票券抽獎：用戶可以使用一定點數參與優惠卷抽獎，抽中的優惠卷可以享受不同程度的折扣（例如9折、85折等），增加用戶參與活動的樂趣。
# 肆、使用工具
使用python建構linebot, 資料庫採用mysql, webhook採用ngrok橋接
