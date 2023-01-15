import { GuildMember, Role } from "discord.js";
import {
  CYN_DISCORD_ID,
  REFOLD_CENTRAL_SERVER_ID,
  REFOLD_JP_SERVER_ID,
  SPARKLES_DISCORD_ID,
  TOAST_DISCORD_ID,
} from "../../constants";

/**
 * Reassigns roles after joining a server for testing purposes
 * @param {GuildMember} member - The member instance who has been banned
 * @returns void
 */
export const reassignRoles = (member: GuildMember) => {
  let role: Role | undefined = undefined;

  if (member.guild.id === REFOLD_CENTRAL_SERVER_ID) {
    switch (member.id) {
      case CYN_DISCORD_ID:
        role = member.guild.roles.cache.find((role) => role.name === "Admin");
        member.roles.add(role as Role);
        break;
      case SPARKLES_DISCORD_ID:
        role = member.guild.roles.cache.find((role) => role.name === "Mod");
        member.roles.add(role as Role);
        break;
      case TOAST_DISCORD_ID:
        role = member.guild.roles.cache.find((role) => role.name === "Mod");
        member.roles.add(role as Role);
        break;
      default:
        return;
    }
  }

  if (member.guild.id === REFOLD_JP_SERVER_ID) {
    switch (member.id) {
      case CYN_DISCORD_ID:
        role = member.guild.roles.cache.find((role) => role.name === "Admin");
        member.roles.add(role as Role);
        role = member.guild.roles.cache.find(
          (role) => role.name === "Staff 本の虫"
        );
        member.roles.add(role as Role);
        break;
      case SPARKLES_DISCORD_ID:
        role = member.guild.roles.cache.find((role) => role.name === "Mod");
        member.roles.add(role as Role);
        role = member.guild.roles.cache.find((role) => role.name === "4段");
        member.roles.add(role as Role);
        break;
      case TOAST_DISCORD_ID:
        role = member.guild.roles.cache.find(
          (role) => role.name === "Network Mod"
        );
        member.roles.add(role as Role);
        role = member.guild.roles.cache.find(
          (role) => role.name === "0段-初心者"
        );
        member.roles.add(role as Role);
      default:
        return;
    }
  }
};
