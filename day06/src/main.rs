use counter::Counter;
use std::fs::File;
use std::io::{
    BufRead,
    BufReader,
    self,
};
use std::path::Path;



/// The output is wrapped in a Result to allow matching on errors
/// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<BufReader<File>>>
    where
        P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(BufReader::new(file).lines())
}



// [Creating a sliding window iterator of slices of chars from a String](https://stackoverflow.com/a/51261570)
/// Trying not to make copies of the original string but rather have pointer into it for the
/// substrings.
fn char_windows<'a>(src: &'a str, win_size: usize) -> impl Iterator<Item = &'a str> {
    src.char_indices()
        .flat_map(move |(from, _)| {
            src[from ..].char_indices()
                .skip(win_size - 1)
                .next()
                .map(|(to, c)| {
                    &src[from .. from + to + c.len_utf8()]
                })
    })
}



fn part_solver(window_size: usize) -> usize {
    let datastream = read_lines("data")
        .unwrap()
        .next()   // Some(Ok("ADFA"))
        .unwrap()   // Ok("ADFA")
        .unwrap()   // "ADFA"
        .chars()
        .collect::<Vec<_>>();
    for (i, window) in datastream.windows(window_size).enumerate() {
        let char_counts = window.iter().collect::<Counter<_>>();
        let by_common = char_counts.k_most_common_ordered(1);   // vec![('c', 3)]
        if by_common[0].1 == 1 {
            return i + window_size;
        }
    }
    0
}



fn part_solver_memory_efficient(window_size: usize) -> usize {
    let datastream = read_lines("data")
        .unwrap()
        .next()   // Some(Ok("ADFA"))
        .unwrap()   // Ok("ADFA")
        .unwrap();   // "ADFA"
    for (i, window) in char_windows(datastream.as_str(), window_size).enumerate() {
        let char_counts = window.chars().collect::<Counter<_>>();
        let by_common = char_counts.k_most_common_ordered(1);   // vec![('c', 3)]
        if by_common[0].1 == 1 {
            return i + window_size;
        }
    }
    0
}





fn main() {
    {
        let answer = part_solver(4);
        println!("Part 1: {}", answer);
        assert!(answer == 1531);
    }
    {
        let answer = part_solver(14);
        println!("Part 2: {}", answer);
        assert!(answer == 2518);
    }
    {
        let answer = part_solver_memory_efficient(4);
        println!("Part 1: {}", answer);
        assert!(answer == 1531);
    }
    {
        let answer = part_solver_memory_efficient(14);
        println!("Part 2: {}", answer);
        assert!(answer == 2518);
    }
}
