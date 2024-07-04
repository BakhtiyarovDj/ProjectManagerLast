const api_url = 'http://localhost:8080';

var global_team_id = ''
async function CreateEmployment() {
    await refreshAccessToken();
    const userData = await getEnteredUsersData();
    if (!userData) return;

    const userId = userData.id;
    const teamListUrl = `${api_url}/users/teamlist/with-user/${userId}`;

    const teamListResponse = await axios.get(teamListUrl, {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    });
    const teamData = teamListResponse.data[0];
    global_team_id = teamData.id
    localStorage.setItem('global_team_id',teamData.id)
    localStorage.setItem('teamTitle', teamData.title); 
    const employmentData = (await axios.get(`${api_url}/users/team-employment/`)).data.filter(item => item.team == global_team_id)

    if (!employmentData.length) {
        try {
            await axios.post(`${api_url}/users/team-employment/`, {
                team: global_team_id,
                status: 'free'
            }, {
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
        } catch (error) {
            console.log(error);
        }
    }
}

CreateEmployment()





async function getEnteredUsersData() {
    const accessToken = localStorage.getItem("access_token");

    try {
        const response = await axios.get(`${api_url}/users/api/userinfo`, {
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        });
        return response.data;
    } catch (error) {
        window.location.href = "../../index.html"
        // console.error('Ошибка при получении информации о пользователе:', error.message);
        return null;
    }
}


document.getElementById('logoutBtn').addEventListener('click', async (event) => {
    await logOut();
});

async function logOut() {
    try {
        const s = await axios.post(`${api_url}/api/logout/`, {
            refresh_token: localStorage.getItem('refresh_token')
        }, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        });
        window.location.href = "../index.html";
    } catch (error) {
        console.error("logout error: ", error);
    }
}

async function refreshAccessToken() {
    const refresh_token = localStorage.getItem('refresh_token');

    try {
        const response = await axios.post(`${api_url}/api/token/refresh/`, {
            refresh: refresh_token
        });

        if (response.status === 200) {
            const new_access_token = response.data.access;
            localStorage.setItem('access_token', new_access_token);
        } else {
            throw new Error('Failed to refresh token');
        }
    } catch (error) {
        window.location.href = "../index.html";
    }
}
