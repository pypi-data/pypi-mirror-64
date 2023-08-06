#include "regex_string.h"
#include <map>
#include <set>
#include <sstream>
#include <tuple>
struct regex_string_value
{
  std::string data;
  std::string name;
};

typedef std::list<regex_string_value> regex_string;
typedef std::unordered_map<std::string, std::string> string_map;

struct regex_value
{
  bool is_op;
  union {
    regex_op op;
    char c;
  } value;
  regex_value() : is_op(true) {}
};

typedef std::list<regex_value> regex_value_list;
typedef std::list<regex_op> op_stack;
typedef std::list<const char> char_stack;
typedef std::map<const char, const char> char_map;

const char_map special_str_{{'w', 'a'}, {'W', '.'}, {'s', ' '}, {'S', 'a'}, {'d', '1'}, {'D', 'a'}, {'l', 'a'}, {'u', 'A'}, {'a', '\a'}, {'f', '\f'}, {'n', '\n'}, {'r', '\r'}, {'t', '\t'}, {'v', '\v'}, {'(', '('}, {')', ')'}, {'{', '{'}, {'}', '}'}, {'[', '['}, {']', ']'}, {'.', '.'}, {'|', '|'}, {'*', '*'}, {'?', '?'}, {'.', '.'}, {'|', '|'}, {'*', '*'}, {'?', '?'}, {'+', '+'}, {'^', '^'}, {'$', '$'}};

inline auto get_spec_str(const char c)
{
  auto iter = special_str_.find(c);
  if (iter != special_str_.end())
  {
    return iter->second;
  }
  return c;
}

inline void push_op(regex_value_list &value_list, regex_op op)
{
  regex_value v;
  v.value.op = op;
  value_list.push_back(v);
}

inline void push_op(regex_value_list &value_list, const char c)
{
  regex_value v;
  v.is_op = false;
  v.value.c = c;
  value_list.push_back(v);
}

inline bool char_is_number(const char c) { return c >= '0' && c <= '9'; }

inline bool char_is_character(const char c)
{
  return (c >= 'a' && c <= 'a') || (c >= 'A' && c <= 'Z');
}

inline void check_index(const char *regex_ptr, std::size_t size,
                        std::size_t index)
{
  if (index >= size)
  {

    throw 1;
  }
}

inline void char_check_number(const char *regex_ptr, std::size_t size,
                              std::size_t index)
{
  check_index(regex_ptr, size, index);
  if (!char_is_number(regex_ptr[index]))
  {

    throw 1;
  }
}

inline void char_check_character(const char *regex_ptr, std::size_t size,
                                 std::size_t index)
{
  check_index(regex_ptr, size, index);
  if (!char_is_character(regex_ptr[index]))
  {

    throw 1;
  }
}

inline void char_check_character(const char *regex_ptr, std::size_t size,
                                 std::size_t index, const char c)
{
  check_index(regex_ptr, size, index);
  if (regex_ptr[index] != c)
  {
    throw 1;
  }
}

inline bool char_is_character(const char *regex_ptr, std::size_t size,
                              std::size_t index, const char c)
{
  check_index(regex_ptr, size, index);
  return regex_ptr[index] == c;
}

#define CHECK_INDEX(index) check_index(regex_ptr, size, index)
#define CHECK_NUMBER(index) char_check_number(regex_ptr, size, index)
#define CHECK_CHARACTER(index, c) \
  char_check_character(regex_ptr, size, index, c)
#define IS_CHARACTER(index, c) char_is_character(regex_ptr, size, index, c)
#define PUSH_OP(op) push_op(value_list, op);
#define PUSHC(index) PUSH_OP(regex_ptr[index])
#define PUSHI(op) \
  PUSH_OP(op);    \
  ++index
#define PUSHCI(index) PUSHI(regex_ptr[index])

inline bool push_char_until(const char *regex_ptr, std::size_t size,
                            std::size_t &index, regex_value_list &value_list,
                            const char c)
{
  auto pre_index = index;
  while (index < size)
  {
    if (regex_ptr[index] == c)
      return true;
    PUSHC(index++);
  }

  throw 1;
  return false;
}

#define PUSH_UNTIL(c) push_char_until(regex_ptr, size, index, value_list, c)

inline bool read_op(const char *regex_ptr, std::size_t size, std::size_t &index,
                    regex_value_list &value_list)
{
  try
  {
    switch (regex_ptr[index])
    {
    case '[':
    {
      if (IS_CHARACTER(index + 1, '^'))
      {
        PUSH_OP(nset_start);
        index += 2;
      }
      else
      {
        PUSHI(set_start);
      }

      bool flag = false;
      for (auto i = index; i < size; i++)
      {
        if (regex_ptr[i] == '-')
        {
          PUSH_OP(set_range);
        }
        else if (regex_ptr[i] == ']')
        {
          PUSH_OP(set_close);
          index = i + 1;
          flag = true;
          break;
        }
        else
        {
          PUSHC(i);
        }
      }
      if (!flag)
      {
      }
    }
    break;
    case '{':
    {
      PUSH_OP(repeat_start);
      bool flag = false;
      for (auto i = index + 1; i < size; i++)
      {
        if (regex_ptr[i] == ',')
        {
          PUSH_OP(repeat_separator);
        }
        else if (regex_ptr[i] == '}')
        {
          PUSH_OP(repeat_close);
          index = i + 1;
          flag = true;
          break;
        }
        else
        {
          CHECK_NUMBER(i);
          PUSHC(i);
        }
      }
      if (!flag)
      {
      }
    }
    break;
    case '(':
    {
      if (IS_CHARACTER(index + 1, '?'))
      {
        index += 2;
        CHECK_INDEX(index);
        switch (regex_ptr[index])
        {
        case '<':
        {
          CHECK_INDEX(++index);
          switch (regex_ptr[index])
          {
          case '=':
          { // (?<=
            PUSHI(look_forward_start);
          }
          break;
          case '!':
          { // (?<!
            PUSHI(look_forward_not_start);
          }
          break;
          default:
          { // (?<name>
            PUSH_OP(name_start);
            PUSH_UNTIL('>');
            PUSHI(name_close);
          }
          break;
          }
        }
        break;
        case '=':
        { // (?=
          PUSHI(look_back_start);
        }
        break;
        case ':':
        { // (?:
          PUSHI(not_match_exp_start);
        }
        break;
        case '!':
        { // (?!
          PUSHI(look_back_not_start);
        }
        break;
        default:
          return false;
        }
      }
      else
      {
        PUSHI(exp_start);
      }
    }
    break;
    case ')':
    {
      PUSHI(exp_close);
    }
    break;
    case '\\':
    {
      PUSHI(trans_char);
      PUSHCI(index);
    }
    break;
    case '*':
    {
      if (IS_CHARACTER(index + 1, '?'))
      {
        PUSH_OP(start_question_mark);
        index += 2;
      }
      else
      {
        PUSHI(star);
      }
    }
    break;
    case '+':
    {
      if (IS_CHARACTER(index + 1, '?'))
      {
        PUSH_OP(add_character_question_mark);
        index += 2;
      }
      else
      {
        PUSHI(add_character);
      }
    }
    break;
    case '|':
    {
      PUSHI(exp_or);
    }
    break;
    default:
    {
      PUSHCI(index);
    }
    break;
    }
  }
  catch (int)
  {
    return false;
  }

  if (index < size)
  {
    if (!read_op(regex_ptr, size, index, value_list))
    {
      return false;
    }
  }

  return true;
}

inline bool compile_regex(const char *regex_ptr, std::size_t size,
                          regex_value_list &ret)
{
  std::size_t index = 0;
  if (!read_op(regex_ptr, size, index, ret))
  {
    return false;
  }
  return true;
}

class bracket_counter
{
public:
  bracket_counter() : _counter(0) {}
  bool count_back(regex_value v)
  {
    if (!v.is_op)
    {
      return false;
    }
    switch (v.value.op)
    {
    case exp_close:
      _counter++;
      break;
    case exp_start:
    case name_start:
    case look_forward_start:
    case look_forward_not_start:
    case look_back_start:
    case look_back_not_start:
    case not_match_exp_start:
      --_counter;
      break;
    }
    return _counter < 0;
  }
  bool count_except_name(regex_value v)
  {
    if (!v.is_op)
    {
      return false;
    }
    switch (v.value.op)
    {
    case exp_close:
      --_counter;
      break;
    case exp_start:
    case look_forward_start:
    case look_forward_not_start:
    case look_back_start:
    case look_back_not_start:
    case not_match_exp_start:
      _counter++;
      break;
    }
    return _counter < 0;
  };
  void reset() { _counter = 0; }

private:
  int32_t _counter;
};
inline void filter_trans_repeat(regex_value_list &value_list)
{
  for (auto iter = value_list.begin(); iter != value_list.end();)
  {
    if (iter->is_op)
    {
      switch (iter->value.op)
      {
      case trans_char:
        iter = value_list.erase(iter);
        if (iter == value_list.end())
          return;
        iter->value.c = get_spec_str(iter->value.c);
        break;
      case star:
      case add_character:
      case add_character_question_mark:
      case start_question_mark:
        iter = value_list.erase(iter);
        break;
      case set_range:
      {
        iter = value_list.erase(iter);
        auto end_value = iter->value.c;
        --iter;
        auto start_value = iter->value.c + 1;
        for (char c = start_value; c < end_value; c++)
        {
          regex_value v;
          v.is_op = false;
          v.value.c = c;
          iter = value_list.insert(iter, v);
        }
      }
      break;
      case repeat_start:
      {
        bool flag = false;
        ++iter;
        while (!(iter->is_op) || iter->value.op != repeat_close)
        {
          if (iter->is_op && iter->value.op == repeat_separator)
          {
            flag = true;
          }
          if (flag)
          {
            iter = value_list.erase(iter);
          }
          else
          {
            ++iter;
          }
        }
      }
      break;
      default:
        ++iter;
        break;
      }
    }
    else
    {
      ++iter;
    }
  }
}
inline void filter_set(regex_value_list &value_list)
{
  for (auto iter = value_list.begin(); iter != value_list.end();)
  {
    if (iter->is_op)
    {
      switch (iter->value.op)
      {
      case set_start:
      {
        iter = value_list.erase(iter);
        ++iter;
        while (!iter->is_op && iter != value_list.end())
          iter = value_list.erase(iter);
        iter = value_list.erase(iter);
      }
      break;
      case nset_start:
      {
        std::set<char> clist;
        iter = value_list.erase(iter);

        while (!iter->is_op && iter != value_list.end())
        {
          clist.insert(iter->value.c);
          iter = value_list.erase(iter);
        }

        for (char c = 0; c <= 0X7F; c++)
        {
          if (clist.find(c) != clist.end())
          {
            continue;
          }
          regex_value v;
          v.is_op = false;
          v.value.c = c;
          value_list.insert(iter, v);
          break;
        }
        iter = value_list.erase(iter);
      }
      break;
      default:
        ++iter;
        break;
      }
    }
    else
    {
      ++iter;
    }
  }
}
inline void filter_or(regex_value_list &value_list)
{
  while (true)
  {
    auto iter = value_list.begin();
    for (; iter != value_list.end(); ++iter)
    {
      if (iter->is_op && iter->value.op == exp_or)
      {
        break;
      }
    }

    if (iter == value_list.end())
    {
      return;
    }

    int32_t counter = 0;
    auto start_iter = iter;
    ++iter;
    for (; start_iter != value_list.begin(); --start_iter)
    {
      if (start_iter->is_op)
      {
        if (start_iter->value.op == exp_start)
        {
          if (--counter < 0)
          {
            ++start_iter;
            for (auto temp_iter = start_iter; temp_iter != iter;)
            {
              temp_iter = value_list.erase(temp_iter);
            }
            break;
          }
        }
        else if (start_iter->value.op == exp_close)
        {
          ++counter;
        }
      }
    }
  }
}
inline void filter_name(regex_value_list &value_list) {}
inline void filter_repeat(regex_value_list &value_list)
{
  auto count = 0;
  for (auto iter = value_list.begin(); iter != value_list.end();)
  {
    if (iter->is_op && iter->value.op == repeat_start)
    {
      std::stringstream ss;
      count = 0;
      iter = value_list.erase(iter); //{
      while (!iter->is_op)
      {
        ss << iter->value.c;
        iter = value_list.erase(iter);
      }
      iter = value_list.erase(iter); // }

      ss >> count;

      auto temp_iter = iter;
      if (temp_iter != value_list.begin())
      {
        for (auto i = 0; i < count - 1; i++)
        {
          if (--temp_iter != value_list.begin() && temp_iter->is_op &&
              temp_iter->value.op == exp_close)
          {
            std::list<regex_value> temp_c;
            temp_c.push_front(*temp_iter);
            bracket_counter counter;
            while (--temp_iter != value_list.begin())
            {
              temp_c.push_front(*temp_iter);
              if (counter.count_back(*temp_iter))
              {
                for (auto &i : temp_c)
                {
                  value_list.insert(iter, i);
                }
                temp_c.clear();
                break;
              }
            }
          }
          else
          {
            value_list.insert(iter, *temp_iter);
          }
          temp_iter = iter;
        }
      }
    }
    else
    {
      ++iter;
    }
  }
}
inline void filter_bracket(regex_value_list &value_list)
{
  bracket_counter counter;
  bool flag = false;
  while (true)
  {
    for (auto iter = value_list.begin(); iter != value_list.end();)
    {
      if (iter->is_op && iter->value.op == exp_start)
      {
        flag = true;
        iter = value_list.erase(iter);
        while (iter != value_list.end() && !counter.count_except_name(*iter))
        {
          ++iter;
        }
        iter = value_list.erase(iter);
        counter.reset();
      }
      else
      {
        ++iter;
      }
    }

    if (!flag)
    {
      break;
    }

    flag = false;
  }
}

inline bool make_regex_string(const char *regex_ptr, std::size_t size,
                              regex_string &rs)
{
  regex_value_list value_list;
  if (!compile_regex(regex_ptr, size, value_list))
  {
    return false;
  }

  // 过滤 ' | '逻辑
  filter_or(value_list);

  // 过滤转义，重复，范围字符
  filter_trans_repeat(value_list);

  // 处理集合
  filter_set(value_list);

  // 对{n}进行重复处理
  filter_repeat(value_list);

  // 去除()分组
  filter_bracket(value_list);

  // 生成regex_string
  for (auto iter = value_list.begin(); iter != value_list.end();)
  {
    if (iter->is_op && iter->value.op == name_start)
    {
      regex_string_value v;
      while ((++iter) != value_list.end() && !iter->is_op)
      {
        v.name.push_back(iter->value.c);
      }

      while ((++iter) != value_list.end() && !iter->is_op)
      {
        v.data.push_back(iter->value.c);
      }

      rs.push_back(v);
    }
    else
    {
      regex_string_value v;
      while ((++iter) != value_list.end() && !iter->is_op)
      {
        v.data.push_back(iter->value.c);
      }
      rs.push_back(v);
    }
  }

  return true;
}

struct regstring::impl
{
  regex_string s;
  std::stringstream ss;
};

regstring::regstring() { impl_ptr = new impl; }

regstring::~regstring()
{
  if (impl_ptr)
  {
    delete impl_ptr;
  }
}

bool regstring::parse_regex(const std::string &regex_str)
{
  impl_ptr->s.clear();
  return make_regex_string(regex_str.c_str(), regex_str.size(), impl_ptr->s);
}

bool regstring::set(const std::string &name, const std::string &data)
{
  if (!impl_ptr)
  {
    return false;
  }

  for (auto &i : impl_ptr->s)
  {
    if (i.name == name)
    {
      i.data = data;
    }
  }

  return true;
}

const char *regstring::c_str()
{
  impl_ptr->ss.str("");
  for (auto &i : impl_ptr->s)
  {
    impl_ptr->ss << i.data;
  }
  return impl_ptr->ss.str().c_str();
}

std::size_t regstring::size() { return impl_ptr->ss.str().size(); }

std::string regstring::str()
{
  impl_ptr->ss.str("");
  for (auto &i : impl_ptr->s)
  {
    impl_ptr->ss << i.data;
  }
  return impl_ptr->ss.str();
}

std::list<std::string> regstring::names()
{
  std::list<std::string> ret;
  for (auto &i : impl_ptr->s)
  {
    if (!i.name.empty())
    {
      ret.push_back(i.name);
    }
  }
  return ret;
}
