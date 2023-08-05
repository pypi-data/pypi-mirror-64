pragma solidity 0.6.4;

import "test/StandardToken.sol";

/*
This Token Contract implements the standard token functionality (https://github.com/ethereum/EIPs/issues/20) as well as the following OPTIONAL extras intended for use by humans.

In other words. This is intended for deployment in something like a Token Factory or Mist wallet, and then used by humans.
Imagine coins, currencies, shares, voting weight, etc.
Machine-based, rapid creation of many tokens would not necessarily need these extra features or will be minted in other manners.

1) Initial Finite Supply (upon creation one specifies how much is minted).
2) In the absence of a token registry: Optional Decimal, Symbol & Name.
3) Optional approveAndCall() functionality to notify a contract if an approval() has occurred.

.*/

contract HumanStandardToken is StandardToken {
    /* Public variables of the token */

    /*
    NOTE:
    The following variables are OPTIONAL vanities. One does not have to include them.
    They allow one to customise the token contract & in no way influences the core functionality.
    Some wallets/interfaces might not even bother to look at this information.
    */
    string public name;                   //fancy name: eg Simon Bucks
    uint8 public _decimals;                //How many decimals to show. ie. There could 1000 base units with 3 decimals. Meaning 0.980 SBX = 980 base units. It's like comparing 1 wei to 1 ether.
    string public symbol;                 //An identifier: eg SBX
    string public version = 'H0.1';       //human 0.1 standard. Just an arbitrary versioning scheme.

    constructor(
        uint256 _initialAmount,
        uint8 _decimalUnits,
        string memory _tokenName,
        string memory _tokenSymbol
    )
        public
    {
        balances[msg.sender] = _initialAmount;               // Give the creator all initial tokens
        _total_supply = _initialAmount;                        // Update total supply
        name = _tokenName;                                   // Set the name for display purposes
        _decimals = _decimalUnits;                            // Amount of decimals for display purposes
        symbol = _tokenSymbol;                               // Set the symbol for display purposes
    }

    /* Approves and then calls the receiving contract */
    function approveAndCall(address _spender, uint256 _value, bytes memory _extraData)
        public
        returns (bool success)
    {
        allowed[msg.sender][_spender] = _value;
        //call the receiveApproval function on the contract you want to be notified. This crafts the function signature manually so one doesn't have to include a contract in here just for this.
        //receiveApproval(address _from, uint256 _value, address _tokenContract, bytes _extraData)
        (bool success, bytes memory data) = _spender.call(abi.encodeWithSignature(
            "receiveApproval(address,uint256,address,bytes)",
            msg.sender,
            _value,
            this,
            _extraData
        ));
        require(success);

        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    fallback () external { revert(); }

    function decimals() public override view returns (uint8 decimals) {
        return _decimals;
    }
}
