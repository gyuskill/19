# 19

nw_diff

## 제목
네트워크 장비 변경 내역 추적 비교

## 개요
네트워크 장비의 구성 변경 내역을 추적하고 비교

시스템 또는 네트워크 구성 변경 사항을 모니터링하거나, 특정 문제가 발생했을 때 그 원인을 찾는데 도움이 된다

작업 사항
* SCP(Secure Copy Protocol)를 사용하여 네트워크 장비에서 백업된 구성 파일의 목록을 추출
* 비교하려는 날짜 범위를 선택할 수 있게 구성
* 사용자가 선택한 날짜 범위 내의 구성 파일들을 비교하고, 변경 사항을 출력
* 'diff' 명령어를 사용하여 구성 파일의 차이를 확인

구현 내용

* 각 함수의 코드 길이와 복잡도를 줄이기 위해 helper 함수를 생성하거나 기존 함수를 분리
-> `select_backup_files`와 `select_backup_date` 함수는 사용자 입력을 처리하는 부분을 독립적인 함수로 분리

* 함수의 파라미터와 반환 값의 명확성을 향상 : `get_file_list` 함수는 시작과 끝 날짜를 인자로 받아 그 사이의 파일들을 리스트로 반환
* Python의 list comprehension을 사용하여 코드를 단순화 : `get_scp_back_dir` 함수와 `get_scp_back_date` 함수

* 코드의 가독성을 높이기 위해 f-string을 사용
-> `print_list` 함수에서 prefix와 items를 출력할 때 사용

* Exception 처리를 개선하여 예외상황에 대한 안정성을 높임
-> `select_backup_files` 함수와 `select_backup_date` 함수에서 입력값 검증과 예외 처리를 통해 프로그램의 안정성을 높임

테스트

1. unittest 모듈을 사용하여 테스트 
2. 각 기능별 테스트
* `test_get_scp_back_dir` : `get_scp_back_dir` 함수를 테스트
-> `@patch` 데코레이터를 사용하여 `os.listdir` 함수를 가상화(Mocking)
-> `['not_scp_backup_from-', 'scp_backup_from-1', 'scp_backup_from-2']` 리스트 반환
-> 반환값이 기대하는 값인 `['scp_backup_from-1', 'scp_backup_from-2']`와 동일한지 확인

* `test_get_scp_back_date` : `get_scp_back_date` 테스트
-> `os.listdir` 함수를 가상화
-> `['file-running-config-20230101_01', 'file-running-config-20230102_02']` 리스트 반환
-> 반환값이 기대하는 값인 `['20230101', '20230102']`와 동일한지 확인

* `test_get_file_date`: `get_file_date` 테스트
-> `get_file_date('file-running-config-20230101_010203')`를 호출
-> 반환값이 기대하는 값인 `datetime.datetime(2023, 1, 1, 1, 2, 3)`와 동일한지 확인
