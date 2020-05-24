# Bank API 
RESTful API to handle Bank Transactions based on Flask, Docker, MongoDB

## Usage
To build docker image:
```
docker-compose build
```
Run api:
```
docker-compose up
```
#### Sending POST requests to:
1\. localhost:5000/register <br />

```json
{
  "username": "username", <!--- BANK, user1, user2 --->
  "password": "password",
  "amount": cash amount <!--- user1, user2 deposit cash amount --->
}
```
Response:
```json
{
  "msg": "You successfully signed up for this API",
  "status": 200
}
```
2\. localhost:5000/balance <br />

```json
{
  "username": "username", <!--- BANK, user1, user2 --->
  "password": "password",
  "amount": cash amount <!--- user1, user2 deposit cash amount --->
}
```
Response:
```json
{
  "Debt": debt amount,
  "Own": cash amount - BANK fee, <!--- user1, user2 deposit cash amount substracted by BANK transaction fee --->
  "Username": "username"
}
```
3\.  localhost:5000/add <br />

```json
{
  "username": "username", <!--- user1, user2 --->
  "password": "password",
  "amount": add cash amount <!--- user1, user2 cash amount to be added to the username account --->
}
```
Response:
```json
{
  "msg": "Amount Added Successfully to account",
  "status": 200
}
```

4\.  localhost:5000/transfer <br />

```json
{
  "username": "username", <!--- user1, user2--->
  "password": "password",
  "to": "username", <!--- user1, user2 --->
  "amount": transfer cash amount <!--- user1, user2 cash amount to transfer --->
}
```
Response:
```json
{
  "msg": "Amount added successfully to account",
  "status": 200
}
```
5\.  localhost:5000/takeloan <br />

```json
{
  "username": "username", <!--- user1, user2 --->
  "password": "password",
  "to": "username", <!--- user1, user2 --->
  "amount": take loan amount <!--- user1, user2 loan to take --->
}
```
Response:
```json
{
  "msg": "Loan Added to Your Account",
  "status": 200
}
```
6\.  localhost:5000/payloan <br />

```json
{
  "username": "username", <!--- user1, user2 --->
  "password": "password",
  "amount": pay loan amount <!--- user1, user2 pay loan (cash amount will be substracted from the username account) --->
}
```
Response:
```json
{
  "msg": "Loan Paid",
  "status": 200
}
```