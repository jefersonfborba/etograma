#!/usr/bin/env python3
"""
Etograma QA - Script de Teste Automatizado
==========================================
Pré-requisitos:
    pip install playwright
    playwright install chromium

Execução:
    python etograma_qa.py

Estratégia por animal:
  1. Instantâneos  : clicar todos simultaneamente (sem espera)
  2. Duração pura  : iniciar todos → aguardar 10s → encerrar todos
  3. Modal         : cada comportamento individualmente, um por vez
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Page, Download

# ─── Configuração ─────────────────────────────────────────────────────────────

URL = "https://jefersonfborba.github.io/etograma/etograma.html"

DURATION_SIMULTANEOUS_WAIT_S = 10   # segundos para fase de duração simultânea
DURATION_INDIVIDUAL_WAIT_S   = 7    # segundos para timers individuais com modal
CLICK_DELAY_MS               = 250  # pausa entre cliques


# ─── Seletores ────────────────────────────────────────────────────────────────

def btn(page: Page, nome: str):
    """Botão de comportamento pelo atributo data-nome (match exato, sem substring)."""
    return page.locator(f'button[data-nome="{nome}"]')

def modal_der_btn(page: Page, text: str):
    """Botão dentro do modal de derivados (#modal-der-chips)."""
    return page.locator("#modal-der-chips").get_by_role("button").filter(has_text=text).first

def modal_alvo_chips(page: Page):
    """Chips de animais no modal de seleção de alvo (#modal-alvo-chips)."""
    return page.locator("#modal-alvo-chips").get_by_role("button")


# ─── Helpers ──────────────────────────────────────────────────────────────────

async def tap(page: Page, text: str, delay: int = CLICK_DELAY_MS):
    """Clica no primeiro botão que contém o texto."""
    await btn(page, text).click()
    await page.wait_for_timeout(delay)


async def select_targets(page: Page, exclude_00: bool = True):
    """
    Seleciona animais no modal de alvo.
    exclude_00=True  → seleciona todos exceto 00
    exclude_00=False → seleciona apenas 00
    """
    chips = modal_alvo_chips(page)
    count = await chips.count()
    for i in range(count):
        chip = chips.nth(i)
        text = await chip.inner_text()
        is_00 = "00" in text
        if exclude_00 and is_00:
            continue
        if not exclude_00 and not is_00:
            continue
        await chip.click()
        await page.wait_for_timeout(150)


async def registrar(page: Page):
    """Clica em Registrar no modal de alvo (#modal-alvo-salvar)."""
    await page.locator("#modal-alvo-salvar").click()
    await page.wait_for_timeout(300)


# ─── Comportamentos com Modal (Duração + Modal) ───────────────────────────────

async def ramoneio_derivado(page: Page, derivado: str):
    """Ramoneio → abre modal → inicia timer → aguarda → encerra."""
    print(f"        Ramoneio → {derivado}")
    # Abrir modal e iniciar timer
    await tap(page, "Ramoneio")
    await modal_der_btn(page, derivado).click()
    await page.wait_for_timeout(DURATION_INDIVIDUAL_WAIT_S * 1000)
    # Abrir modal novamente e encerrar
    await tap(page, "Ramoneio")
    await modal_der_btn(page, derivado).click()
    await page.wait_for_timeout(400)


async def allogrooming(page: Page):
    """Allogrooming → seleciona animais → Registrar → aguarda → encerra."""
    print("        Allogrooming")
    await tap(page, "Allogrooming")
    await select_targets(page, exclude_00=True)
    await registrar(page)
    await page.wait_for_timeout(DURATION_INDIVIDUAL_WAIT_S * 1000)
    await tap(page, "Allogrooming")


async def perseguir(page: Page):
    """Perseguir → seleciona animais → Registrar → aguarda → encerra."""
    print("        Perseguir")
    await tap(page, "Perseguir")
    await select_targets(page, exclude_00=True)
    await registrar(page)
    await page.wait_for_timeout(DURATION_INDIVIDUAL_WAIT_S * 1000)
    await tap(page, "Perseguir")


# ─── Comportamentos com Modal (Apenas Instantâneos) ───────────────────────────

async def contato_derivado(page: Page, derivado: str):
    print(f"        Contato → {derivado}")
    await tap(page, "Contato")
    await modal_der_btn(page, derivado).click()
    await page.wait_for_timeout(400)
    await select_targets(page, exclude_00=True)
    await registrar(page)


async def brincadeira_derivado(page: Page, derivado: str, only_00: bool = False):
    print(f"        Brincadeira → {derivado}")
    await tap(page, "Brincadeira")
    await modal_der_btn(page, derivado).click()
    await page.wait_for_timeout(400)
    await select_targets(page, exclude_00=not only_00)
    await registrar(page)


async def deslocar(page: Page):
    print("        Deslocar outro animal")
    await tap(page, "Deslocar outro animal")
    await select_targets(page, exclude_00=True)
    await registrar(page)


async def ameaca_derivado(page: Page, derivado: str):
    print(f"        Ameaça → {derivado}")
    await tap(page, "Ameaça")
    await modal_der_btn(page, derivado).click()
    await page.wait_for_timeout(400)
    await select_targets(page, exclude_00=True)
    await registrar(page)


async def snapping(page: Page):
    print("        Snapping")
    await tap(page, "Snapping")
    await select_targets(page, exclude_00=True)
    await registrar(page)


async def relincho_derivado(page: Page, derivado: str):
    print(f"        Relincho → {derivado}")
    await tap(page, "Relincho")
    await modal_der_btn(page, derivado).click()
    await page.wait_for_timeout(400)


# ─── Ciclo por Animal ─────────────────────────────────────────────────────────

async def test_animal(page: Page, animal_id: str):
    """Executa o ciclo completo de observação para um animal."""
    print(f"\n{'═' * 52}")
    print(f"  Animal {animal_id}")
    print('═' * 52)

    # Selecionar animal na barra superior
    await page.get_by_role("button", name=f"🏷️ {animal_id}").click()
    await page.wait_for_timeout(500)

    # ── FASE 1: Instantâneos ─────────────────────────────────
    print("\n  [1/3] Instantâneos (todos de uma vez)")
    for nome in ["Empinar", "Bocejar", "Micção", "Defecação", "Guincho", "Resfôlego"]:
        await btn(page, nome).click()
        await page.wait_for_timeout(200)

    # ── FASE 2: Duração Pura (simultânea) ────────────────────
    print("\n  [2/3] Duração pura (simultânea)")
    duracoes = [
        "Ingestão de água",
        "Fuga",
        "Dormir",
        "Coçar em objeto",
        "Espojar",
        "Grooming",
        "Mastigação não nutritiva",
    ]

    print("    → Iniciando todos os timers...")
    for nome in duracoes:
        await btn(page, nome).click()
        await page.wait_for_timeout(200)

    print(f"    → Aguardando {DURATION_SIMULTANEOUS_WAIT_S}s...")
    await page.wait_for_timeout(DURATION_SIMULTANEOUS_WAIT_S * 1000)

    print("    → Encerrando todos os timers...")
    for nome in duracoes:
        await btn(page, nome).click()
        await page.wait_for_timeout(200)

    # ── FASE 3: Modal (sequencial) ───────────────────────────
    print("\n  [3/3] Comportamentos com modal (um por vez)")

    await ramoneio_derivado(page, "Arbusto")
    await ramoneio_derivado(page, "Árvore")
    await ramoneio_derivado(page, "Raiz")

    await allogrooming(page)

    await contato_derivado(page, "Cabeça-corpo")
    await contato_derivado(page, "Nariz-corpo")
    await contato_derivado(page, "Nariz-nariz")

    await brincadeira_derivado(page, "Locomotora")
    await brincadeira_derivado(page, "Luta")
    await brincadeira_derivado(page, "Objeto", only_00=True)

    await deslocar(page)

    await ameaca_derivado(page, "Coicear")
    await ameaca_derivado(page, "Morder")

    await perseguir(page)

    await snapping(page)

    await relincho_derivado(page, "Normal")
    await relincho_derivado(page, "Suave")
    await relincho_derivado(page, "Longo")

    print(f"\n  ✅ Animal {animal_id} concluído!")


# ─── Setup ────────────────────────────────────────────────────────────────────

async def setup(page: Page):
    """Configura o ambiente do zero: usuário, projeto e animais."""
    print("🔧 Setup: navegando e limpando cache...")
    await page.goto(URL)
    await page.evaluate("""async () => {
        const regs = await navigator.serviceWorker.getRegistrations();
        for (const reg of regs) await reg.unregister();
        const keys = await caches.keys();
        for (const key of keys) await caches.delete(key);
        localStorage.clear();
        sessionStorage.clear();
    }""")
    await page.reload()
    await page.wait_for_load_state("networkidle")

    # Usuário
    print("🔧 Setup: criando usuário...")
    await page.get_by_role("textbox").fill("Usuário Teste")
    await page.get_by_role("button", name="Confirmar").click()
    await page.wait_for_timeout(500)

    # Projeto
    print("🔧 Setup: criando projeto...")
    await page.get_by_role("button", name="＋ Novo Projeto").click()
    await page.wait_for_timeout(300)
    await page.get_by_placeholder("Ex: Pasto Norte").fill("Projeto Teste")
    await page.get_by_role("button", name="Criar").click()
    await page.wait_for_timeout(500)

    # Cadastros: 13 animais (00–12)
    print("🔧 Setup: adicionando 13 animais (00–12)...")
    await page.get_by_role("button", name="⚙️ Cadastros").click()
    await page.wait_for_timeout(500)
    for i in range(13):
        await page.get_by_role("button", name="Adicionar animal").click()
        await page.wait_for_timeout(200)
        await page.get_by_placeholder("Ex: Preto").fill(f"{i:02d}")
        await page.get_by_role("button", name="Confirmar").click()
        await page.wait_for_timeout(250)

    # Navegar para Registrar
    print("🔧 Setup: navegando para Registrar...")
    await page.get_by_role("button", name="☰").click()
    await page.wait_for_timeout(300)
    await page.get_by_role("button", name="🏠 Início").click()
    await page.wait_for_timeout(300)
    await page.get_by_role("button", name="📋 Registrar").click()
    await page.wait_for_timeout(500)

    print("✅ Setup concluído!\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

DOWNLOADS_DIR = Path(__file__).parent / "downloads"

async def handle_download(download: Download) -> None:
    """Salva qualquer download feito pelo usuário na pasta ./downloads/."""
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    dest = DOWNLOADS_DIR / download.suggested_filename
    await download.save_as(dest)
    print(f"\n  📥 Arquivo salvo em: {dest}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        # Intercepta downloads e salva em pasta conhecida
        page.on("download", lambda d: asyncio.ensure_future(handle_download(d)))

        await setup(page)

        # Animais 01–12
        for i in range(1, 13):
            await test_animal(page, f"{i:02d}")

        print("\n🎉 Teste completo para todos os 12 animais!")
        print("   Verifique os registros nas abas 'Registros' e 'Resumo'.")
        print("\n   Pressione ENTER para fechar o navegador...")
        await asyncio.get_event_loop().run_in_executor(None, input)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
