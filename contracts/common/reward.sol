// SPDX-License Identifier: GPL-3.0

pragma solidity ^0.8.24;

import "./account.sol";

library Reward {
    uint constant base_reward_every_minutes = 60;
    uint constant base_reward_tokens = 1;

    function calculate_reward(AccountStruct memory user) private view returns (uint)  {
        uint last_updated = user.last_updated;
        if (last_updated == 0) {
            return 0;
        }

        uint reward_quantity = (block.timestamp - last_updated) / ((base_reward_every_minutes - user.selling_time_upgrade) * 60);

        uint user_mining_power = user.mining_power_upgrade;
        if (user_mining_power > 0) {
            user_mining_power -= 1;
        }
        uint tokens_per_reward = ((base_reward_tokens/100) * (100 + (user_mining_power) *10));

        return ((base_reward_every_minutes - user.selling_time_upgrade +1) * reward_quantity) * 60;
    }
}