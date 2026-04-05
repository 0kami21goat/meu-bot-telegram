from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

import os

TOKEN = os.getenv("TOKEN")

# ========= TEXTO PRINCIPAL =========
def texto_menu():
    return """Olá 👋

Eu sou o Jack Cyber, assistente oficial da JC Network.

Aqui você pode contratar Internet SSH/VPN, IPTV, fazer recargas com desconto, renovar seu acesso ou receber suporte automático.

⚡ Atendimento 24 horas
💳 Pagamentos via PIX
🚀 Liberação rápida

Escolha uma opção abaixo:"""

# ========= MENU PRINCIPAL =========
def menu_principal():
    botoes = [
        [InlineKeyboardButton("🌐 Internet SSH / VPN", callback_data="internet")],
        [InlineKeyboardButton("📺 IPTV", callback_data="iptv")],
        [InlineKeyboardButton("💳 Recargas", callback_data="recargas")],
        [InlineKeyboardButton("💼 Revenda", callback_data="revenda")],
        [InlineKeyboardButton("🛠 Suporte", callback_data="suporte")],
        [InlineKeyboardButton("👨‍💻 Falar com Atendente", callback_data="atendimento")]
    ]
    return InlineKeyboardMarkup(botoes)

# ========= TELAS =========
def tela_internet():
    texto = """🌐 Internet SSH/VPN

✔ Redes sociais
✔ Vídeos
✔ Jogos leves
✔ Uso diário

Depende do sinal da operadora."""
    botoes = [
        [InlineKeyboardButton("🧪 Fazer Teste", url="https://servex.ws/test/655607db-9a6c-43b6-9813-c122b93efc0d")],
        [InlineKeyboardButton("🛒 Comprar/Renovar Internet", url="https://servex.ws/loja/4022ee5c-3811-4847-a277-820746e0c900")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
    ]
    return texto, InlineKeyboardMarkup(botoes)
 
def tela_iptv():
    texto = """📺 IPTV

📺 Canais ao vivo
🎬 Filmes
📺 Séries
🎭 Novelas"""
    botoes = [
        [InlineKeyboardButton("🛒 Comprar IPTV", url="https://api.whatsapp.com/send?phone=5521959173752&text=Tenho%20interesse%20em%20adquirir%20a%20IPTV%20%F0%9F%93%BA.%20Pode%20me%20explicar%20como%20funciona%20e%20como%20fa%C3%A7o%20para%20contratar%3F%20%F0%9F%A4%94%F0%9F%93%B2")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
    ]
    return texto, InlineKeyboardMarkup(botoes)

def tela_recargas():
    texto = """💳 Recargas com desconto

⏱ Prazo médio: até 2 horas
⚠ Pode levar até 24h em instabilidade."""
    botoes = [
        [InlineKeyboardButton("📲 Fazer Recarga", url="https://recargasdigital.site/recarga/?revendedor=1772304862000")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
    ]
    return texto, InlineKeyboardMarkup(botoes)

def tela_revenda():
    texto = "💼 Revenda\n\nGanhe dinheiro revendendo nossos serviços."
    botoes = [
        [InlineKeyboardButton("📞 Solicitar Informações", callback_data="atendimento")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
    ]
    return texto, InlineKeyboardMarkup(botoes)

def tela_suporte():
    texto = "🛠 Suporte\n\nSelecione uma opção abaixo."
    botoes = [
        [InlineKeyboardButton("👨‍💻 Falar com Suporte", callback_data="atendimento")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
    ]
    return texto, InlineKeyboardMarkup(botoes)

def tela_atendimento():
    texto = "👨‍💻 Atendimento JC Network"
    botoes = [
        [InlineKeyboardButton("📞 WhatsApp", url="https://wa.me/5521959173752")],
        [InlineKeyboardButton("💬 Telegram", url="https://t.me/JC_Networkk")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
    ]
    return texto, InlineKeyboardMarkup(botoes)

# ========= GERENCIADOR =========
async def mostrar_menu(update, context):
    chat_id = update.effective_chat.id

    try:
        await update.message.delete()
    except:
        pass

    if "menu_id" in context.user_data:
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=context.user_data["menu_id"],
                text=texto_menu(),
                reply_markup=menu_principal()
            )
            return
        except:
            pass

    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=texto_menu(),
        reply_markup=menu_principal()
    )
    context.user_data["menu_id"] = msg.message_id

# ========= START =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update, context)

# ========= CALLBACK =========
async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    telas = {
        "internet": tela_internet,
        "iptv": tela_iptv,
        "recargas": tela_recargas,
        "revenda": tela_revenda,
        "suporte": tela_suporte,
        "atendimento": tela_atendimento
    }

    if query.data == "voltar":
        await query.edit_message_text(
            texto_menu(),
            reply_markup=menu_principal()
        )
    elif query.data in telas:
        texto, markup = telas[query.data]()
        await query.edit_message_text(texto, reply_markup=markup)

# ========= EXECUÇÃO =========
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(botoes))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mostrar_menu))

app.run_polling()
