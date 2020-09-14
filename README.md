# DA Software exam (Sep 2020)


## How to pull/use my code

- I used [Docker](https://hub.docker.com/repository/docker/shnlee622/gs_sep2020) and [Github](https://github.com/shnlee-ds/gs_swtest_sep2020) and my DockerHub is connected to GitHub, thus it is automatically building the docker image. Please run the below command to pull the docker image.

```bash
docker pull shnlee622/gs_sep2020:latest
```

- Codes in this repo were all copied in the docker image so you can simply run the image to use this program. The image also includes 'sample.txt' that contains the list of test cases. 


- Since'view.py' is an interactive interface, please add '-it' option when running the docker image.

```
docker run -it shnlee622/gs_sep2020
```

- When you enter '0' to exit 'view.py', the docker container will also be closed. Since the output data are created inside the container, please use 'docker cp' command to move the ouput data into your local machine or add '-v' option to link the local host when running the docker image.



## Software Design summary

- I used MVC pattern to implement this interface, and used Command-Line Interface to enable users to add data and get statistics from the data.

- Allergy or Claim Type should be only entered from a given category list. Medical Condition is also allowed to input only as ICD-10 code, a standardized medical classification code. This is for an efficiency of the future analysis based on well categorized data.

- SSN was used as an individual identifier. However, SSN has a security issue, so the hash value of SSN was used as the policy holder's ID. SSN is required when adding a new data, but the hash-converted ID is displayed instead of SSN when displaying a data list.


### Test cases

- When 'view.py' is running, you can see an interactive interface like the above screenshot. You can add a new policy holder or a claim history by entering '1' or '2', and below are the test cases. Test cases are also stored in 'sample.txt'.

```
- Successful cases for adding policy holder
(1) Female, 06/03/1992, 172-01-0201, Y, Pet/Food, M54.2
(2) Male, 12/08/1996, 101-16-6062, N, Insect, M99.01 
(3) Male, 03/21/1973, 741-11-2321, Y, Drug, G44.311

- Failure cases for adding policy holder
(1) Wrong date format: Female, 06-03-1992, 172-01-0201, Y, Pet/Food, M54.2
(2) Wrong SSN format: Female, 06/03/1992, 172010201, Y, Pet/Food, M54.2
(3) Out of Allergy category: Female, 06/03/1992, 172-01-0201, Y, Dog, M54.2
(4) Out of ICD-10 code (Medical condition): Female, 06/03/1992, 172-01-0201, Y, Pet/Food, Covid-19
```
- 아래는 policy holder 등록시에 발생할 수 있는 오류들을 보여주는 failure cases 들이다.
```
failure case - 간략한 이유와 함께
```

- 2를 누르면 claim 정보를 추가할 수 있다. 마찬가지로 success and failure cases
```
success samples
```
```
failure case - 간략한 이유와 함께
```

- 3을 누르면 SSN을 입력하고 해당 unique ID를 찾을 수 있다.

- 4부터 9까지는 데이터에서 간단한 통계나 집계를 얻을 수 있는 메뉴이다. 데이터가 비어있을때는 경고 메시지를 띄운다.
