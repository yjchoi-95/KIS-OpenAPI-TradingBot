#  📈 KIS-OpenAPI-TradingBot

<p align="center">
  <img src="https://github.com/user-attachments/assets/178cff23-cb42-45a7-83a9-ac29af443425" width="30%" />
</p>

- 본 프로젝트는 한국투자증권 DX-Community(동아리) 활동의 일환으로 진행된 것으로, 한국투자증권의 공식 문서가 아님을 안내드립니다.
<br/>

## 💡 개요
- 주제 : AI 기반 KOSPI 지수 등락 예측·매매 자동화 프로그램 구축
  - 데이터 수집/전처리 → 익일 코스피 지수 상승/하락 예측 모델링 → 예측 결과 활용한 자동 매매 까지의 **프로토 타입** 구축
  - (예시) **매일** 오전 08:30 당일 **KOSPI200 지수의 등락 예측 결과** 확인, 조건에 따라 **자동으로** ACE 200 ETF와 ACE 인버스 ETF를 **매매**
 
## 🚀 진행과정

- 데이터 수집
  - 한국투자증권 OpenAPI(KIS Developers)를 활용한 데이터 수집
    - [📍 한국투자증권 OpenAPI Github](https://github.com/koreainvestment/open-trading-api) [📍 한국투자증권 OpenAPI 홈페이지](https://apiportal.koreainvestment.com/about)  
  - 수집 데이터 : **국내주식업종기간별시세(일/주/월/년)** 

<p align="center">
   <img src="https://github.com/user-attachments/assets/48a4ee13-b3dd-438a-a0c1-af14aa20dc33" width="60%" />
</p>
    
- 데이터 정제
  - Feature Engineering 수행
    - 독립 변수 변환 : Classifier 구축 시 지표 데이터 → 등락률 변환
    - 기술적 지표 추가 : Pandas ta 라이브러리 활용 
  - 수집 원천 데이터 → M/L, D/L 모델 입력에 맞게 Feature 변환하는 Class 작성
    - M/L - 데이터 : **`DataPreprocessor'**
    - D/L - 데이터 : **`transform_for_dl'** (추후 개발)
   
- AI 모델링
  - M/L : AutoML, LightGBM, CyclicBoosting
  - D/L : Pre-trained model 활용 (추후 개발)
  
- 예측 결과 활용
  - OpenAPI 활용 자동 매매
    - 매매 조건: Model Confidence 0.75 이상, N개의 모델* 중 70% 이상이 동일한 결과 출력 등 (* M/L 모델의 기술적 지표 알고리즘 활용)
    - 당일 매매 조건에 대한 OpenAPI 자동 매매
    - 예측 결과 및 매매 진행 상황 slack message 발송 (추후 개발)

- 배치 프로세스 수행을 통한 자동화
  - Local Airflow를 활용하여 배치 자동화
  - 데이터 수집 ~ 매매까지의 각 프로세스 DAG화  

<br/>

## 📂 디렉토리 구조

📂 KIS-OpenAPI-TradingBot  
│  
├── 📂 .ipynb_checkpoints  
├── 📂 __pycache__  
├── 📂 config  
│   └── config_vts.yaml  # API KEY, 계좌번호 등 개인정보  
│  
├── 📂 data  
│   ├── deomesticindex.xlsx  
│   ├── ds_domesticIndex_flaml.pkl  
│   ├── ml_flaml_lgbm_domesticIndex.pkl  
│   └── rs_domesticIndex.pkl  
│  
├── 📂 logs  
│   └── ml_flaml_lgbm.log  
│  
├── 📂 scripts  
│   ├── 📂 origin  
│   │   ├── 국내업종기간별시세_20241110.ipynb  
│   │   ├── 국내업종기간별시세_20241120.ipynb  
│   │   ├── 국내주식분봉조회_20241110.ipynb  
│   │   ├── 금리종합_20241110.ipynb  
│   │   ├── 자동매매샘플코드_20241212.ipynb  
│   │   └── 종합시황공시_20241119.ipynb  
│   ├── dxcai_domestic_index_trading_dag.ipynb  
│   ├── dxcai_extract_DomesticIndex.ipynb  
│   ├── dxcai_ml_DomesticIndex_lightgbm.ipynb  
│   ├── dxcai_preproc_DomesticIndex_ml_lightgbm.ipynb  
│   ├── utils.py  
│   └── 자동매매샘플코드_20241212.ipynb  
│  
├── 📂 tokens  
│   ├── token.json  
│   └── token_dev.json  
└── 📄 README.md  

