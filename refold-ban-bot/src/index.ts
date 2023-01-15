import "dotenv/config";
import { Client, GatewayIntentBits, TextChannel } from "discord.js";
import { initializeWinston } from "./setup/initializeWinston";
import { getChannel } from "./helpers/getChannel";
import { reassignRoles } from "./helpers/guildMemberAdd";
import {
  getServersUserIsBannedFrom,
  sendMessageToBanLogChannel,
} from "./helpers/guildBanAdd";

const winston = initializeWinston();

winston.log("info", "Bot is starting...");

const botIntents: Array<GatewayIntentBits> = [
  GatewayIntentBits.Guilds,
  GatewayIntentBits.GuildMessages,
  GatewayIntentBits.MessageContent,
  GatewayIntentBits.GuildBans,
  GatewayIntentBits.GuildMembers,
];

const client = new Client({
  intents: botIntents,
});

client.on("messageCreate", async (message) => {
  if (message.content === "42d1964e-c93a-43aa-be35-211b3436b7c4") {
    await message.member?.ban({ reason: "Test" });

    setTimeout(async () => {
      await message.guild?.members.unban(message.author.id);
    }, 5000);
  }
});

client.on("guildMemberAdd", async (member) => {
  await member.guild.roles.fetch();
  reassignRoles(member);
});

client.on("guildBanAdd", async (currentBan) => {
  const serversUserIsBannedFrom = getServersUserIsBannedFrom(
    client,
    currentBan
  );

  client.guilds.cache.forEach(async (guild) => {
    const banLogChannel = getChannel(guild, "ban-bot-log");

    if (!banLogChannel) {
      winston.log("error", "There was no ban-bot-log channel found.");
      return;
    }

    if (banLogChannel.isTextBased()) {
      const members = await guild.members.fetch();
      const userIsBannedFromAnotherGuild = members.find(
        (member) => member.id === currentBan.user.id
      );

      if (userIsBannedFromAnotherGuild) {
        sendMessageToBanLogChannel(
          banLogChannel as TextChannel,
          currentBan,
          serversUserIsBannedFrom
        );
      }
    }
  });
});

client.on("ready", () => {
  winston.log("info", "Bot is ready");
});

client.login(process.env.DISCORD_BOT_TOKEN);
