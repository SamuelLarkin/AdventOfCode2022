use std::fs::File;
use std::io::{
    BufRead,
    BufReader,
    Read,
    Result,
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



/// Parse the input data and returns a list of bags.
fn get_bags() -> Vec<Vec<u32>> {
    let mut bags: Vec<Vec<u32>> = vec![];
    let mut bag: Vec<u32> = vec![];
    for line in read_lines("data").unwrap() {
        if let Ok(calory) = line {
            if calory == "" {
                bags.push(bag);
                bag = vec![];
            }
            else {
                bag.push(calory.parse::<u32>().unwrap());
            }
        }
    }
    bags.push(bag);
    //println!("bags: {:?}", bags);
    //println!("bags: {:?}", bags.len());

    bags
}



#[derive(Debug)]
pub struct Paragraphs<B> {
    buf: B,
}

impl<B: BufRead> Iterator for Paragraphs<B> {
    type Item = Result<Vec<String>>;

    fn next(&mut self) -> Option<Result<Vec<String>>> {
        let mut paragraph: Vec<String> = vec![];
        let mut buf = String::new();
        loop {
            let n = self.buf.read_line(&mut buf);
            //println!("l {:?}  buf {:?}", n, buf);
            match n {
                Ok(0) => return None,
                Ok(_n) => {
                    if buf.ends_with('\n') {
                        buf.pop();
                        if buf.ends_with('\r') {
                            buf.pop();
                        }
                    }
                    if buf == "" {
                        return Some(Ok(paragraph));
                    }
                    else {
                        paragraph.push(String::from(buf.as_str()));
                        buf.clear();
                    }
                }
                //Err(e) => Some(Err(e)),
                Err(_e) => return None,
            };
        }
    }
}

pub trait Paragraphable : Read {
    fn paragraphs(self) -> Paragraphs<Self>
        where 
            Self: Sized;
}

impl<R> Paragraphable for BufReader<R>
    where
        R: Read,
    {
    fn paragraphs(self) -> Paragraphs<Self> {
        Paragraphs { buf: self }
    }
}



/// How many total Calories is that Elf carrying?
fn part1() -> u32 {
    let bags = get_bags();
    let calories: Vec<u32> = bags
        .iter()
        .map(|bag| bag.iter().sum())
        .collect();
    //println!("calories: {:?}", calories);

    calories
        .into_iter()
        .max()
        .unwrap()
}



fn part1_p(filename: &str) -> u32 {
    let file = File::open(filename).unwrap();
    BufReader::new(file)
        .paragraphs()
        .map(Result::unwrap)
        .map(|bag| bag
            .iter()
            .map(|v| v.parse::<u32>().unwrap())
            .sum())
        .max()
        .unwrap()
}



/// How many Calories are those Elves carrying in total?
fn part2() -> u32 {
    let bags = get_bags();
    let mut calories: Vec<u32> = bags
        .iter()
        .map(|bag| bag.iter().sum())
        .collect();

    // Sort in decreasing order.
    calories.sort_by(|a, b| b.cmp(a));
    calories
        .into_iter()
        .take(3)
        .into_iter()
        .sum::<u32>()
}



fn part2_p(filename: &str) -> u32 {
    let file = File::open(filename).unwrap();
    let mut bags: Vec<u32> = BufReader::new(file)
        .paragraphs()
        .map(Result::unwrap)
        .map(|bag| bag
            .iter()
            .map(|v| v.parse::<u32>().unwrap())
            .sum())
        .collect();
    bags.sort_by(|a, b| b.cmp(a));
    bags
        .into_iter()
        .take(3)
        .into_iter()
        .sum()
}



fn main() {
    let filename = "data";

    {
        let answer = part1();
        println!("Part1: {}", answer);
        assert!(answer == 69289);
    }

    {
        let answer = part2();
        println!("Part2: {}", answer);
        assert!(answer == 205615);
    }

    {
        // Are we able to iterate properly over paragraphs?
        let filename = "data";
        let file = File::open(filename).unwrap();
        for p in BufReader::new(file).paragraphs() {
            println!("{:?}", p);
        }
    }

    {
        // Solution for part 1 using paragraph iterator.
        let answer = part1_p(filename);
        println!("Part 1: {}", answer);
        assert!(answer == 69289);
    }

    {
        // Solution for part 2 using paragraph iterator.
        let answer = part2_p(filename);
        println!("Part 1: {}", answer);
        assert!(answer == 205615);
    }
}
