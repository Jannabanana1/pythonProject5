// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/access/AccessControl.sol"; //This allows role-based access control through _grantRole() and the modifier onlyRole
import "@openzeppelin/contracts/token/ERC20/ERC20.sol"; //This contract needs to interact with ERC20 tokens

contract AMM is AccessControl{
    bytes32 public constant LP_ROLE = keccak256("LP_ROLE");
  uint256 public invariant;
  address public tokenA;
  address public tokenB;
  uint256 feebps = 3; //The fee in basis points (i.e., the fee should be feebps/10000)

  event Swap( address indexed _inToken, address indexed _outToken, uint256 inAmt, uint256 outAmt );
  event LiquidityProvision( address indexed _from, uint256 AQty, uint256 BQty );
  event Withdrawal( address indexed _from, address indexed recipient, uint256 AQty, uint256 BQty );

  /*
    Constructor sets the addresses of the two tokens
  */
    constructor( address _tokenA, address _tokenB ) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender );
        _grantRole(LP_ROLE, msg.sender);

    require( _tokenA != address(0), 'Token address cannot be 0' );
    require( _tokenB != address(0), 'Token address cannot be 0' );
    require( _tokenA != _tokenB, 'Tokens cannot be the same' );
    tokenA = _tokenA;
    tokenB = _tokenB;

    }


  function getTokenAddress( uint256 index ) public view returns(address) {
    require( index < 2, 'Only two tokens' );
    if( index == 0 ) {
      return tokenA;
    } else {
      return tokenB;
    }
  }

  /*
    The main trading functions
    
    User provides sellToken and sellAmount
    The contract must calculate buyAmount using the formula:
  */
  function tradeTokens( address sellToken, uint256 sellAmount ) public {
    require( invariant > 0, 'Invariant must be nonzero' );
    require( sellToken == tokenA || sellToken == tokenB, 'Invalid token' );
    require( sellAmount > 0, 'Cannot trade 0' );
    require( invariant > 0, 'No liquidity' );
    uint256 qtyA;
    uint256 qtyB;
    uint256 swapAmt; // balance of B minus delta B

    //YOUR CODE HERE 
    if(sellToken == tokenA){
      qtyA =  ERC20(tokenA).balanceOf(address(this)) + sellAmount; 
      qtyB = (10000+feebps) * invariant/(qtyA * 10000);
      swapAmt = ERC20(tokenB).balanceOf(address(this)) - qtyB;

      ERC20(tokenA).transferFrom( msg.sender, address(this), sellAmount);
      ERC20(tokenB).transfer(msg.sender, swapAmt);
    }
    else{
      qtyB =  ERC20(tokenB).balanceOf(address(this)) + sellAmount; 
      qtyA = (10000+feebps) * invariant/(qtyB * 10000);
      swapAmt = ERC20(tokenA).balanceOf(address(this)) - qtyA;

      ERC20(tokenB).transferFrom( msg.sender, address(this), sellAmount);
    invariant = ERC20(tokenA).balanceOf(address(this))*ERC20(tokenB).balanceOf(address(this));
    emit Withdrawal( msg.sender, recipient, amtA, amtB );
  }


}
