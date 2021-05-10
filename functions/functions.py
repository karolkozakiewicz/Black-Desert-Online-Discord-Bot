import logging
import discord

def assign_data(ctx):
    data = {}
    try:
        data['server_name'] = ctx.guild.name
    except:
        data['server_name'] = None
    try:
        data['channel_name'] = ctx.channel.name
    except:
        data['channel_name'] = None
    try:
        data['author_nick'] = ctx.author.nick
    except:
        data['author_nick'] = None
    try:
        data['author_name'] = ctx.author.name
    except:
        data['author_name'] = None
    try:
        data['server_id'] = ctx.guild.id
    except:
        data['server_id'] = None
    try:
        data['channel_id'] = ctx.channel.id
    except:
        data['channel_id'] = None
    try:
        data['author_id'] = ctx.author.id
    except:
        data['author_id'] = None
    try:
        data['attachment_url'] = ctx.attachments[0].url
    except:
        data['attachment_url'] = None
    try:
        data['message'] = str(ctx.content)
    except:
        data['message'] = None
    return data

# def whosonline(ctx, bot, server_id):
#
#     print(ctx.guild.id)
#
#
#     # moj_id = ctx.author.id
#     #
#     # nazwy_roli = ", ".join([str(r.name) for r in ctx.guild.roles])
#     # channels_names = (", ".join([str(r.name) for r in ctx.guild.channels]))
#     # ids = [int(r.id) for r in ctx.guild.channels]
#     #
#     # output = []
#     # beautiful_output = ""
#     # for channel_id in ids:
#     #
#     #     try:
#     #         channel = bot.get_channel(channel_id)  # gets the channel you want to get the list from
#     #         if str(channel.type) == 'voice':
#     #             members = channel.members  # finds members connected to the channel
#     #             mem_name = [member.display_name for member in members]
#     #             mem_ids = [member.id for member in members]
#     #             if len(mem_ids) != 0:
#     #                 output.append([channel.name, mem_name])
#     #     except Exception as e:
#     #         logging.info(e)
#     # for x in output:
#     #     beautiful_output += f"{x[0]}: {x[1]}\n"
#     # if len(beautiful_output) < 1:
#     #     beautiful_output += "Brak danych"
#     # print(beautiful_output)
#     # # return (beautiful_output)