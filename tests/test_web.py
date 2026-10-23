import os
import unittest


os.environ.setdefault("FLASK_SECRET_KEY", "chave-exclusiva-para-testes-automatizados")
os.environ.setdefault("ADMIN_PASSWORD", "senha-exclusiva-para-testes")

from sistema_ponto.web import app  # noqa: E402


class WebAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_pagina_de_ponto_abre(self):
        resposta = self.client.get("/ponto")
        self.assertEqual(resposta.status_code, 200)

    def test_admin_exige_login(self):
        resposta = self.client.get("/admin")
        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])

    def test_login_incorreto_nao_autentica(self):
        resposta = self.client.post(
            "/login",
            data={"senha": "incorreta"},
            follow_redirects=True,
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Senha incorreta".encode(), resposta.data)

    def test_login_correto_libera_admin(self):
        resposta = self.client.post(
            "/login",
            data={"senha": os.environ["ADMIN_PASSWORD"]},
            follow_redirects=True,
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Painel administrativo".encode(), resposta.data)


if __name__ == "__main__":
    unittest.main()
