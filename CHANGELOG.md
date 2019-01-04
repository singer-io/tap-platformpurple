# Changelog

## 1.0.2

- Paginate by hour instead of per day [#2](https://github.com/singer-io/tap-platformpurple/pull/2)

## 1.0.1

- Merge 0.0.4 into 1.0.0

## 1.0.0

- Initial Release

## 0.0.4

- Add Products endpoint
- Add missing fields to Events, Transactions endpoints

## 0.0.3

- Don't advance state file past current date
- Add pagination-related logs
- Upgrade tap-framework from 0.0.4 to 0.0.5

## 0.0.2

- Fix datetime comparison for state files
- Fix pagination strategy (microseconds get dropped from query)

## 0.0.1

- First Version
