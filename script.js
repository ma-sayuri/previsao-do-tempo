// PASSO 1 saber quando o btn for clicado - e ao ser clicado, chamar função
// PASSO 2 pegar texto (cidade) dentro do input
// PASSO 3 ir no servidor e pegar os dados do tempo atualizados
// PASSO 4 organizar as informações do tempo que chegaram
// PASSO 5 colocar informações na tela

let chave = "cebcd482eda57fa9a6714c1c2ba91885"

function colocarNaTela(dados) {
    console.log(dados);

    // verifica se a resposta da API contém um código de erro
    if (dados.cod === "404") {
        // caso a cidade não for encontrada, é exibida uma mensagem de erro 
        alert("Cidade não encontrada. Por favor, verifique se o nome da cidade está correto e tente novamente.");
        return;
    }

    // atualização dos dados do tempo na interface do usuário
    document.querySelector('.cidade').innerHTML = 'Tempo em ' + dados.name
    document.querySelector('.temp').innerHTML = Math.floor(dados.main.temp) + '°C' // Math.floor -> ferramenta do JS pra arredondar valores 
    document.querySelector('.icone').src = "https://openweathermap.org/img/wn/" + dados.weather[0].icon + ".png"
    document.querySelector('.umidade').innerHTML = 'Umidade: ' + dados.main.humidity + '%'
    document.querySelector('.vento').innerHTML = 'Velocidade do Vento: ' + dados.wind.speed + ' km/h';
    document.querySelector('.ceu').innerHTML = traducaoCeu(dados.weather[0].description);
}

// função pra traduzir a descrição do céu para pt
function traducaoCeu(descricao) {
    switch (descricao) {
        case 'clear sky':
            return 'Céu limpo';
        case 'few clouds':
            return 'Poucas nuvens';
        case 'scattered clouds':
            return 'Nuvens dispersas';
        case 'broken clouds':
            return 'Nuvens quebradas';
        case 'overcast clouds':
            return 'Nublado';
        case 'light rain':
            return 'Chuva fraca';
        case 'moderate rain':
            return 'Chuva moderada';
        case 'heavy intensity rain':
            return 'Chuva intensa';
        default:
            return '';
    }
}

async function buscarCidade(cidade){
    let dados = await fetch(  // FETCH -> Ferramenta do JS para acessar servidores
        'https://api.openweathermap.org/data/2.5/weather?q=' +
            cidade +
            '&appid=cebcd482eda57fa9a6714c1c2ba91885&units=metric',
    ).then((resposta) => resposta.json())

    colocarNaTela(dados)
}

function clickedBtn(){
    let cidade = document.querySelector(".input-cidade").value

    buscarCidade(cidade)
}

