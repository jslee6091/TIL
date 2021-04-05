1. 커피 주문을 처리하는 MS

   - 사용자 요청으로 전달 된 커피 주문을 ORDER MS의 DB에 저장

   - endpoint: GET /order-ms/[user_id]/orders/

     - 주문 목록 보기

   - endpoint: GET /order-ms/[user_id]/orders/[order_id]

     - 주문 상세 보기

   - endpoint: POST /order-ms/[user_id]/orders/

     ```json
     {
         "coffee_name": "today's coffee",
         "coffee_price": "5000",
         "coffee_qty": "3"
     }
     ```

   - 추가된 주문 정보를 kafka에 전송

2. ORDER MS에 전달 된 커피 주문 정보를 ORDER DELIVERY MS로 전달

   - ORDER MS의 DB에 저장된 커피 정보를 ORDER DELIVERY MS의 DB에 저장
   - endpoint: GET /delivery-ms/[status]
     - 현재 status(접수완료 ...)에 있는 주문을 모두 표시
   - endpoint: GET /delivery-ms/[user_id]/[order_id]
     - 커피의 주문 상태를 표시 ex) 접수완료, 제작중, 배송완료, 취소 ...