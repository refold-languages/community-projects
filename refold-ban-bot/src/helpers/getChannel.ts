import { Guild, GuildBasedChannel } from "discord.js";

/**
 * Gets a channel from a guild
 * @param {Guild} guild - The guild to get the channel from
 * @param {string} channelName - The name of the channel
 * @returns {GuildBasedChannel | undefined} The channel instance
 */
export const getChannel = (
  guild: Guild,
  channelName: string
): GuildBasedChannel | undefined => {
  return guild.channels.cache.find((channel) => channel.name === channelName);
};
