function handleAPIResponse(response) {
    if (response.status === 401 || response.status === 403) {
        return response.json().then(data => {
            alert(data.error);
            window.location.href = data.redirect;
            throw new Error(data.error);  // 에러를 발생시켜 후속 처리를 중단합니다.
        });
    }
    return response;  // 정상 응답인 경우 원래의 response를 반환합니다.
}

// 다른 스크립트에서 이 함수를 사용할 수 있도록 export합니다.
export { handleAPIResponse };