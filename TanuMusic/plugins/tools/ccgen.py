import random
from pyrogram import filters
from TanuMusic import app

def luhn(n):
    r = [int(ch) for ch in str(n)][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

def gen_cc(bin_prefix, count=10):
    results = []
    for _ in range(count):
        num = bin_prefix
        while len(num) < 15:
            num += str(random.randint(0,9))
        for d in range(10):
            candidate = num + str(d)
            if luhn(candidate):
                results.append(candidate)
                break
    return results

@app.on_message(filters.command(["ccgen", "gencc"]))
async def ccgen_cmd(client, message):
    args = message.text.split()
    if len(args) < 2:
        return await message.reply("Usage: /ccgen <bin> [count]")
    bin_p = args[1][:6]
    count = int(args[2]) if len(args) > 2 else 10
    count = min(count, 20)
    ccs = gen_cc(bin_p, count)
    text = "**Generated CCs:**\n" + "\n".join(f"`{c}`" for c in ccs)
    await message.reply(text)
