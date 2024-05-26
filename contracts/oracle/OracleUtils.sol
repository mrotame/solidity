// SPDX-License-Identifier: MIT

pragma solidity 0.8.24;

library OracleUtils {
    function transferEther( address _to, uint _weiAmount) internal{
        (bool success, ) = payable(_to).call{value: _weiAmount}("");
        require(success, "TransferEther Error: failed to call receiver");
    }
}