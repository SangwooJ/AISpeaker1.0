# AISpeaker1.0
BS graduation project

Paper : [Dropbox](https://www.dropbox.com/s/9k7go29plrda5lv/%ED%95%99%EC%82%AC%ED%95%99%EC%9C%84%EB%85%BC%EB%AC%B8_%EC%A0%84%EC%83%81%EC%9A%B0.pdf?dl=0)


Inroduction : 사용자에게 인공지능을 활용한 다양한 서비스를 음성으로, 쉽고 편리하게 제공해주는 웹 기반의 서비스를 구현하고자 하였다. 사용자는 PC 또는 모바일 기기의 웹 브라우저를 통해 로그인하여 서비스를 이용할 수 있다. 본 서비스는 사용자의 질문을 음성을 통해 인식하여 날씨, 뉴스, 증권, 성경에 관련한 응답을 음성과 함께 제공해준다. 웹은 python 기반의 웹 프레임워크인 Django 를 사용하였다. 질문의 의도 파악은 Attention 모델을 통해 분류 모델을 구현하였고, 본문에 관한 질의 응답은 BERT 모델을 적용하였다. 웹 서비스가 사용자의 대용량 request 에 대해서도 Scalability, Robustness 를 유지할 수 있도록 시스템 아키텍처에 로드 밸런싱을 적용하였다. 또한 초기의 monolithic 시스템 구조를 기능별로 재설계하여 Micro Service Architecture 로 개선하였다.
