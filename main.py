from logging import PlaceHolder
import discord, asyncio, datetime, os
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.errors import CommandOnCooldown

client = commands.Bot(command_prefix ='.')
client.remove_command("help")
token = 'TOKEN'

@client.event
async def on_ready():
    print("running\n---- ---- ---- ----")
    print("Servers connected to :")
    for guild in client.guilds:
        print(str(guild.name) + " / " + str(guild.id))
#        print(str(guild.text_channels) + "\n")
        print("---- ---- ---- ---- ---- ---- ---- ----")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="[.도움]을 통하여 모든 명령어를 확인해보세요!"))

async def on_reaction_add(reaction, user):
    if not isinstance(reaction.message.channel, discord.DMChannel):
        return

@client.command(pass_context=True)
async def 도움(ctx):
    embed = discord.Embed(
            title="<:purple_moonstar:985856301890412575> 봇 도움말",
            description="[디스보드](https://disboard.org)) | [한디리(한국 디스코드 리스트)](https://koreanbots.dev)", #추가필요
            color=0xeeeee0
        )
    embed.add_field(name="제보 명령어", value="`.익명(.익) [할말]\n.노익명(.노익) [할말]`")
#    embed.set_footer(text="디스코드 대신 전해드림")
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def 서버정보(ctx):
    if ctx.guild.id == YOUR_GUILD_ID_HERE:
        embed = discord.Embed(
                title="서버정보",
                description="",
                color=0x62D0F6
            )
        embed.add_field(name="⌨️ 서버 이름", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name="🗓️ 서버 생성일", value=f"{ctx.guild.created_at}", inline=True)
        embed.add_field(name="🙇‍♂️ 서버 소유자", value=f"<@{ctx.guild.owner_id}>", inline=True)
        embed.add_field(name="💎 서버 부스트 / 티어", value=f"{ctx.guild.premium_subscription_count}개 / **Level {ctx.guild.premium_tier}**", inline=True)
        embed.add_field(name="👋 멤버 수", value=f"{ctx.guild.member_count}", inline=True)
        embed.add_field(name="🔒 인증레벨", value=f"{ctx.guild.verification_level}", inline=True)
        embed.add_field(name="💿 업로드 가능한 파일 사이즈", value=f"{ctx.guild.filesize_limit} Byte", inline=True)
        embed.add_field(name="🗃️ 업로드 가능한 최대 이모지 수", value=f"{ctx.guild.emoji_limit}", inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send("⚠️ 해당 봇은 **__디스코드 대신 전해드림__** 서버에서만 사용할수 있습니다.")

# 제보
@client.command(pass_context=True, aliases=['익'])
@commands.dm_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def 익명(ctx, *, args):
    if discord.ChannelType.private:
        ok = discord.Embed(
            title="✅ 메시지 전송 성공!",
            description="익명채널에 성공적으로 전송되었습니다.\n만약 오류가 발생하여 전송이 안됐다면 서버 내에 있는 티켓을 이용하여 관리자를 호출해 주세요.\n\n> 전송된 내용 :\n> " + str(args),
            color = 0xFC9630
        )
        await ctx.reply(embed=ok)
        embed = discord.Embed(
                title=":pencil2: 익명 제보입니다.",
                description=str(args),
                color=0xFFB900
        )
        embed.set_footer(text="전송된 시간 : " + str(datetime.datetime.now()))
        channel = client.get_channel(PRIVATE_CHANNEL_ID) #익명제보채널
        reaction2 = await channel.send(embed=embed)
        log = client.get_channel(SEND_LOG_CHANNEL_ID) #제보로그
        anembed = discord.Embed(
                title="익명제보 로그",
                description=f":pencil: 제보자 : {ctx.author} ({ctx.author.id})\n:clock1: 제보 시간 : {datetime.datetime.now()}\n\n:newspaper: 제보 내용 :\n{args}",
                color=0xcceecc
            )
        await log.send(embed=anembed)
        print(f"익명제보 전송됨 ({datetime.datetime.now()})")
        ## 이모지 임시 비활성화 (서버마다 다름)
        #await reaction2.add_reaction("<:like:983697036253757450>")
        #await reaction2.add_reaction("<:love:983697038405410886>")
        #await reaction2.add_reaction("<:cheerup:983697030541111296>")
        #await reaction2.add_reaction("<:haha:983697032847970354>")
        #await reaction2.add_reaction("<:wow:983697043866402846>")
        #await reaction2.add_reaction("<:sad:983697041064615946>")
        #await reaction2.add_reaction("<:fbangry:983697027999350824>")

@client.command(pass_context=True, aliases=['ㄴ', '노익'])
@commands.dm_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def 노익명(ctx, *, args):
    if discord.ChannelType.private:
        ok = discord.Embed(
            title="✅ 메시지 전송 성공!",
            description="노익명 채널에 성공적으로 전송되었습니다.\n만약 오류가 발생하여 전송이 안됐다면 서버 내에 있는 티켓을 이용하여 관리자를 호출해 주세요.\n\n> 전송된 내용 :\n> " + str(args),
            color = 0xFC9630
        )
        await ctx.reply(embed=ok)
        embed = discord.Embed(
                title=":pencil2: [" + str(ctx.author) + "] 님의 제보입니다.",
                description=str(args),
            color=0x339EFF
            )
        embed.set_footer(text="전송된 시간 : " + str(datetime.datetime.now()))
        channel = client.get_channel(PUBLIC_CHANNEL_ID) #노익명제보채널
        reaction2 = await channel.send(embed=embed)
        log = client.get_channel(SEND_LOG_CHANNEL_ID) #제보로그
        pubembed = discord.Embed(
                title="노익명제보 로그",
                description=f":pencil: 제보자 : {ctx.author} ({ctx.author.id})\n:clock1: 제보 시간 : {datetime.datetime.now()}\n\n:newspaper: 제보 내용 :\n{args}",
                color=0xddaadd
            )
        await log.send(embed=pubembed)
        print(f"노익명제보 전송됨 ({datetime.datetime.now()})")
        ## 이모지 임시 비활성화 (서버마다 다름)
        #await reaction2.add_reaction("<:like:983697036253757450>")
        #await reaction2.add_reaction("<:love:983697038405410886>")
        #await reaction2.add_reaction("<:cheerup:983697030541111296>")
        #await reaction2.add_reaction("<:haha:983697032847970354>")
        #await reaction2.add_reaction("<:wow:983697043866402846>")
        #await reaction2.add_reaction("<:sad:983697041064615946>")
        #await reaction2.add_reaction("<:fbangry:983697027999350824>")

# discord.ext.commands.errors.CommandInvokeError: Command raised an exception: AttributeError: 'PrivateMessageOnly' object has no attribute 'send'
@익명.error
async def 제보_error(error, ctx):
    if not isinstance(error, commands.PrivateMessageOnly):
        embed = discord.Embed(
                title=":warning: Error",
                description="**__봇 오류가 발생하였습니다. DM 여부와 내용이 작성되었는지 확인해 보세요!**",
                color=0xffffff
            )
        await error.reply(embed=embed)

@노익명.error
async def 제보_error(error, ctx):
    if not isinstance(error, commands.PrivateMessageOnly):
        embed = discord.Embed(
                title=":warning: Error",
                description="**__봇 오류가 발생하였습니다. DM 여부와 내용이 작성되었는지 확인해 보세요!**",
                color=0xffffff
            )
        await error.reply(embed=embed)

client.run(token)
