import { AuditLogEvent, Client, GuildBan, TextChannel } from "discord.js";
import { initializeWinston } from "../../setup/initializeWinston";

const winston = initializeWinston();

/**
 * Gets the servers that a user is banned from
 * @param {Client} client - The Discord client instance
 * @param {GuildBan} currentBan - The currently banned user instance
 * @returns {string[]} list of servers a user is banned from
 */
export const getServersUserIsBannedFrom = (
  client: Client,
  currentBan: GuildBan
): string[] => {
  let serversUserIsBannedFrom: string[] = [];

  client.guilds.cache.forEach(async (guild) => {
    const currentServerBanList = await guild.bans.fetch();
    const userHasBeenBannedFromServer = currentServerBanList.find(
      (bannedMember) => bannedMember.user.id === currentBan.user.id
    );

    if (userHasBeenBannedFromServer) {
      serversUserIsBannedFrom.push(guild.name);
    }
  });

  return serversUserIsBannedFrom;
};

/**
 * Gets the mod who banned the user
 * @param {GuildBan} currentBan - The currently banned user instance
 * @returns the user instance who banned the currently banned user
 */
export const getModWhoBannedUser = async (currentBan: GuildBan) => {
  const guildUserWasBannedFrom = currentBan.guild;
  const fetchedLogs = await guildUserWasBannedFrom.fetchAuditLogs({
    limit: 1,
    type: AuditLogEvent.MemberBanAdd,
  });

  // Since there's only 1 audit log entry in this collection, grab the first one
  // and return the user object instance who banned the member
  return fetchedLogs.entries.first();
};

/**
 * Sends the message to the ban log channel
 * @param {TextChannel} banLogChannel - The channel to send the message to
 * @param {GuildBan} currentBan - The currently banned user instance
 * @param {string[]} serversUserIsBannedFrom - List of servers the user is currently banned from
 * @returns Promise<void>
 */
export const sendMessageToBanLogChannel = async (
  banLogChannel: TextChannel,
  currentBan: GuildBan,
  serversUserIsBannedFrom: string[]
): Promise<void> => {
  const modWhoBannedUser = await getModWhoBannedUser(currentBan);

  // Perform a coherence check to make sure that there's *something*
  if (!modWhoBannedUser) {
    winston.log(
      "info",
      `${currentBan.user.tag} was banned from ${currentBan.guild.name} but no audit log could be found.`
    );
    return;
  }

  await banLogChannel.send(
    `<@${currentBan.user.id}> was banned from the ${
      currentBan.guild.name
    } server. \n Banned by: <@${modWhoBannedUser.executor?.id}> \n Reason: ${
      currentBan.reason || "No reason provided."
    } \n Servers banned from: ${serversUserIsBannedFrom}`
  );
  console.log(
    `<@${currentBan.user.id}> got hit with the swift hammer of justice in the guild ${currentBan.guild.name}, wielded by the mighty ${modWhoBannedUser.executor?.tag}`
  );
};
