import 'dart:convert';

String vulnerabilitaJson = '''{
    "Nome": "SQL Injection",
    "Categoria": "Injection",
    "Severita": "Alta",
    "Descrizione": "Consente l'esecuzione di query SQL malevole"
  },
  {
    "Nome": "Cross-Site Scripting (XSS)",
    "Categoria": "Client-side",
    "Severita": "Media",
    "Descrizione": "Permette l'iniezione di script nel browser della vittima"
  },
  {
    "Nome": "Cross-Site Request Forgery (CSRF)",
    "Categoria": "Session Management",
    "Severita": "Media",
    "Descrizione": "Induce l'utente autenticato a eseguire richieste non volute"
  },
  {
    "Nome": "Broken Authentication",
    "Categoria": "Authentication",
    "Severita": "Alta",
    "Descrizione": "Debolezze nei meccanismi di login e gestione sessione"
  }
''';

class Vulnerabilita {
  final String nome;
  final String categoria;
  final String severita;
  final String descrizione;

  Vulnerabilita(this.nome, this.categoria, this.severita, this.descrizione);
  Vulnerabilita.fromJson(Map<String, dynamic> json)
    : nome = json['Nome'],
      categoria = json['Categoria'],
      severita = json['Severita'],
      descrizione = json['Descrizione'];
}

class ListaVulnerabilita {
  final List<Vulnerabilita> lista;
  ListaVulnerabilita({required this.lista});

  factory ListaVulnerabilita.fromJson(List<dynamic> parsedJson) {
    List<Vulnerabilita> lista = parsedJson
        .map((vuln) => Vulnerabilita.fromJson(vuln))
        .toList();
    return ListaVulnerabilita(lista: lista);
  }
}

void main(List<String> args) {
  print("Trasforma in lista di classe Vulnerabilita da stringa json");
  List<dynamic> vulnerabilitaMap = jsonDecode('[$vulnerabilitaJson]');
  List<Vulnerabilita> vulnerabilita = ListaVulnerabilita.fromJson(vulnerabilitaMap).lista;

  for (final v in vulnerabilita) {
    print('${v.nome}, ${v.categoria}, ${v.severita}, ${v.descrizione}');
  }
}
