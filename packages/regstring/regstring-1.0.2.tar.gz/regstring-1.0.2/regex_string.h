#pragma once
#include <cstddef>
#include <list>
#include <string>
#include <unordered_map>
enum regex_op
{
  set_start = 0,                    // [     ===>  [a-zA-Z0-9]
  nset_start = 1,                   // [^    ===>  [^a-zA-Z0-9]
  set_range = 2,                    // -     ===>  [a-zA-Z0-9] or [^a-zA-Z0-9]
  set_close = 3,                    // ]     ===>  [a-zA-Z0-9] or [^a-zA-Z0-9]
  repeat_start = 4,                 // {     ===>  {n1, n2} or {n}
  repeat_separator = 5,             // ,     ===>  {n1, n2}
  repeat_close = 6,                 // }     ===>  {n1, n2} or {n}
  exp_start = 7,                    // (     ===>  (exp|exp)
  exp_or = 8,                       // |     ===>  (exp|exp)
  name_start = 9,                   // (?<   ===>  (?<name>exp)
  name_close = 10,                  // >     ===>  (?<name>exp)
  look_forward_start = 11,          // (?<=  ===>  (?<=exp)
  look_forward_not_start = 12,      // (?<!  ===>  (?<!exp)
  look_back_start = 13,             // (?=   ===>  (?=exp)
  look_back_not_start = 14,         // (?!   ===>  (?!exp)
  not_match_exp_start = 15,         // (?:   ===>  (?:exp)
  exp_close = 16,                   // ）    ===>   )
  star = 17,                        // *     ===>   exp*
  add_character = 18,               // +     ===>   exp+
  start_question_mark = 19,         // *?    ===>   exp*?
  add_character_question_mark = 20, // +?    ===>   exp+?
  trans_char = 21,                  // \     ===>   \{
};

class regstring
{
public:
  regstring();
  ~regstring();

  bool parse_regex(const std::string &regex_str);
  bool set(const std::string &name, const std::string &data);

  const char *c_str();
  std::size_t size();
  std::string str();

  std::list<std::string> names();

private:
  struct impl;
  impl *impl_ptr;
};